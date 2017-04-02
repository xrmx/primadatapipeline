package main

import (
	"bytes"
	"encoding/json"
    "math/rand"
	"net/http"
	"strings"
	"time"
)

type Sale struct {
	Ts string `json:"timestamp"`
    // money in cents as we don't have decimals in stdlib
	Amount int32 `json:"amount"`
	PaymentType string `json:"payment_type"`
}

func dailySalesHandler(response http.ResponseWriter, request *http.Request) {
	request.ParseForm()
    day := strings.Join(request.Form["day"], "")
	t, _ := time.Parse("2006-01-02", day)
    secs := t.Unix()

	var sales [10]Sale
	for i := 0; i < 10; i++ {
		var payment string
		if i % 2 == 0 {
			payment = "cash"
		} else {
			payment = "card"
		}
		ts := time.Unix(secs + int64(3600 * i), 0)
		sales[i] = Sale{ts.Format(time.RFC3339), rand.Int31()/10000, payment}
	}
	response_data, _ := json.Marshal(sales)
	buf := bytes.NewBuffer(response_data)
	response.Write(buf.Bytes())
}

func main() {
	http.HandleFunc("/dailysales", dailySalesHandler)
	http.ListenAndServe(":8888", nil)
}
