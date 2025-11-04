$Headers = @{"X-Gitlab-Token"=""}
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