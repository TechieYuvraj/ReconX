def export_urls(visited):
    with open("visited_urls.txt", "w") as file:
        for url in visited:
            file.write(url + "\n")
    print("[✓] URLs exported to visited_urls.txt")