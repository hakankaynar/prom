
## Nice prometheus queries
rate(app_requests_count_total[1m])

rate(app_request_latency_sum[1m])/rate(app_request_latency_count[1m])