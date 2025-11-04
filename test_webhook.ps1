$Headers = @{"X-Gitlab-Token"="glpat-ZGQ1TBZDwPZ8FYQixdBoh286MQp1OmlvcXloCw.01.120ld8rp0"}
$Body = @{
    object_kind = "merge_request"
    object_attributes = @{
        iid = "1"
        title = "Test PR"
        changes_count = "10"
    }
    user = @{
        username = "test_user"
    }
}
$JsonBody = ConvertTo-Json $Body
Invoke-RestMethod -Uri "http://localhost:8080/api/gitlab/webhook" -Method POST -Headers $Headers -ContentType "application/json" -Body $JsonBody