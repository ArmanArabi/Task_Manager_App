# get all tasks without auth    
def test_tasks_list_response_401(anon_client):
    response = anon_client.get('/tasks')
    assert response.status_code == 401
   
    
# authrizaed user , return tasks
def test_tasks_list_response_200(auth_client):
    response = auth_client.get('/tasks')
    print(f' ****** \n RESPONSE: {response.json()} \n ******* ')
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    
# authrizaed user , return a exist random task
def test_tasks_detail_response_200(auth_client, random_task):
    task_obj = random_task
    response = auth_client.get(f'/tasks/{task_obj.id}')
    assert response.status_code == 200
    assert len(response.json()) > 0


# authrizaed user , return a not exist random task
def test_tasks_detail_response_404(auth_client):
    response = auth_client.get(f'/tasks/{100}')
    assert response.status_code == 404
    