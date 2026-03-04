import requests

# 1. Виконання GET-запиту
print("--- GET Request ---")
get_url = "https://jsonplaceholder.typicode.com/posts/1"
get_response = requests.get(get_url)

print(f"Статус-код: {get_response.status_code}")
print("Заголовки відповіді:")
for key, value in get_response.headers.items():
    print(f"  {key}: {value}")

print("\nТіло відповіді (JSON):")
print(get_response.json())
print("-" * 30)

# 2. Виконання POST-запиту
print("\n--- POST Request ---")
post_url = "https://jsonplaceholder.typicode.com/posts"
new_post_data = {
    "title": "Мій новий пост",
    "body": "Це тестове повідомлення, яке відправляється через POST.",
    "userId": 1
}

post_response = requests.post(post_url, json=new_post_data)

print(f"Статус-код: {post_response.status_code}")
print("Заголовки відповіді:")
for key, value in post_response.headers.items():
    print(f"  {key}: {value}")

print("\nТіло відповіді (створений ресурс):")
print(post_response.json())