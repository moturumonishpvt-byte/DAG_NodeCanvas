from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_api():
    # Valid payload
    payload = {
        "nodes": [{"id": "1"}, {"id": "2"}],
        "edges": [{"source": "1", "target": "2"}]
    }
    response = client.post(
        "/pipelines/parse",
        data={"pipeline": json.dumps(payload)}
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"num_nodes": 2, "num_edges": 1, "is_dag": True}
    print("API test passed for valid payload")

    # Invalid payload (malformed JSON)
    response2 = client.post(
        "/pipelines/parse",
        data={"pipeline": "not_a_json"}
    )
    assert response2.status_code == 400
    print("API test passed for malformed JSON")
    
    # Missing nodes or edges
    payload_invalid = {"nodes": "not_a_list", "edges": []}
    response3 = client.post(
        "/pipelines/parse",
        data={"pipeline": json.dumps(payload_invalid)}
    )
    assert response3.status_code == 400
    print("API test passed for invalid types")

if __name__ == "__main__":
    test_api()
    print("All API tests passed!")
