package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"
)

// Структуры данных
type RouterLoadRequest struct {
	ApplicationID   int             `json:"application_id"`
	TotalUsers      int             `json:"total_users"`
	Routers         []RouterInfo    `json:"routers"`
	AuthToken       string          `json:"auth_token"`
	CallbackURL     string          `json:"callback_url"` // URL для отправки результатов
}

type RouterInfo struct {
	ID          int `json:"id"`
	MasterID    int `json:"master_id,omitempty"`
	CurrentLoad int `json:"current_load,omitempty"`
}

type RouterUpdate struct {
	RouterID   int `json:"router_id"`
	RouterLoad int `json:"router_load"`
}

type UpdatePayload struct {
	MasterRouterID int `json:"master_router_id,omitempty"`
	RouterLoad     int `json:"router_load,omitempty"`
}

// Константы
const (
	Port         = ":9000"
	DjangoURL    = "http://localhost:8080"
	ServiceToken = "async_secret_token_2025"
	DelaySeconds = 7
)

func main() {
	http.HandleFunc("/calculate-router-load", calculateRouterLoad)
	http.HandleFunc("/health", healthCheck)
	
	fmt.Printf("Асинхронный сервис запущен на порту %s\n", Port)
	log.Fatal(http.ListenAndServe(Port, nil))
}

func healthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "ok",
		"service": "async-router-load-calculator",
	})
}

func calculateRouterLoad(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var request RouterLoadRequest
	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// Проверка токена
	if request.AuthToken != ServiceToken {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Логируем начало расчета
	log.Printf("Starting calculation for application %d with %d users and %d routers", 
		request.ApplicationID, request.TotalUsers, len(request.Routers))

	// ВАЖНО: Сразу возвращаем ответ клиенту (Django), чтобы не было таймаута
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":           "calculation_started",
		"application_id":   request.ApplicationID,
		"message":          "Расчет нагрузки запущен в фоновом режиме",
	})

	// Запускаем расчет в отдельной горутине (фоном)
	go func(req RouterLoadRequest) {
		// Имитируем задержку расчета
		delay := DelaySeconds + rand.Intn(3) // 7-10 секунд
		time.Sleep(time.Duration(delay) * time.Second)

		// Выполняем расчет нагрузки
		results := calculateLoadDistribution(req.TotalUsers, req.Routers)

		// Отправляем результаты в Django
		updateRouterLoadsInDjango(req.ApplicationID, results, req.CallbackURL)
		
		log.Printf("Calculation completed for application %d", req.ApplicationID)
	}(request)
}

func calculateLoadDistribution(totalUsers int, routers []RouterInfo) []RouterUpdate {
	var results []RouterUpdate
	
	// Группируем роутеры по наличию нагрузки
	routersWithLoad := make([]RouterInfo, 0)
	routersWithoutLoad := make([]RouterInfo, 0)
	sumExistingLoad := 0
	
	for _, router := range routers {
		if router.CurrentLoad > 0 {
			routersWithLoad = append(routersWithLoad, router)
			sumExistingLoad += router.CurrentLoad
		} else {
			routersWithoutLoad = append(routersWithoutLoad, router)
		}
	}
	
	// Если есть роутеры без нагрузки, распределяем оставшихся пользователей
	if len(routersWithoutLoad) > 0 {
		if sumExistingLoad <= totalUsers {
			remainingUsers := totalUsers - sumExistingLoad
			
			if remainingUsers > 0 {
				// Базовое распределение
				baseLoad := remainingUsers / len(routersWithoutLoad)
				remainder := remainingUsers % len(routersWithoutLoad)
				
				// Случайное распределение остатка
				rand.Seed(time.Now().UnixNano())
				indices := rand.Perm(len(routersWithoutLoad))
				
				for i, idx := range indices {
					router := routersWithoutLoad[idx]
					load := baseLoad
					
					// Добавляем остаток первым N роутерам
					if i < remainder {
						load++
					}
					
					// Добавляем случайную вариацию ±20%
					variation := int(float64(load) * 0.2)
					if variation > 0 {
						load += rand.Intn(variation*2+1) - variation
					}
					
					// Убеждаемся, что нагрузка не отрицательная
					if load < 0 {
						load = 0
					}
					
					results = append(results, RouterUpdate{
						RouterID:   router.ID,
						RouterLoad: load,
					})
				}
			} else {
				// Нет пользователей для распределения
				for _, router := range routersWithoutLoad {
					results = append(results, RouterUpdate{
						RouterID:   router.ID,
						RouterLoad: 0,
					})
				}
			}
		}
	}
	
	// Добавляем роутеры с существующей нагрузкой
	for _, router := range routersWithLoad {
		results = append(results, RouterUpdate{
			RouterID:   router.ID,
			RouterLoad: router.CurrentLoad,
		})
	}
	
	return results
}

func updateRouterLoadsInDjango(appID int, results []RouterUpdate, callbackURL string) {
	// Обновляем каждый роутер через соответствующий endpoint
	for _, result := range results {
		// Создаем payload для обновления
		payload := UpdatePayload{
			RouterLoad: result.RouterLoad,
		}
		
		// Конвертируем в JSON
		jsonData, err := json.Marshal(payload)
		if err != nil {
			log.Printf("Error marshaling payload for router %d: %v", result.RouterID, err)
			continue
		}
		
		// Формируем URL для обновления конкретного роутера
		url := fmt.Sprintf("%s/api/AddedRouters/change/%d/", DjangoURL, result.RouterID)
		
		// Создаем запрос
		req, err := http.NewRequest("PUT", url, bytes.NewBuffer(jsonData))
		if err != nil {
			log.Printf("Error creating request for router %d: %v", result.RouterID, err)
			continue
		}
		
		// Добавляем заголовки
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("X-Async-Service-Token", ServiceToken)
		
		// Отправляем запрос
		client := &http.Client{Timeout: 10 * time.Second}
		resp, err := client.Do(req)
		if err != nil {
			log.Printf("Error updating router %d: %v", result.RouterID, err)
			continue
		}
		
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			log.Printf("Failed to update router %d. Status: %d", result.RouterID, resp.StatusCode)
		} else {
			log.Printf("Successfully updated router %d with load %d", result.RouterID, result.RouterLoad)
		}
		
		resp.Body.Close()
		
		// Небольшая задержка между запросами, чтобы не перегружать Django
		time.Sleep(100 * time.Millisecond)
	}
	
	log.Printf("Completed updating %d routers for application %d", len(results), appID)
}