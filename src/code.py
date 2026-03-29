import random
import networkx as nx
import matplotlib.pyplot as plt


def validate_parameters(N, M, K):
    if N <= 0 or N > 50:
        raise ValueError("Liczba przystanków N musi być dodatnia i mniejsza lub równa 50.")
    if M < N - 1 or M > 100:
        raise ValueError("Liczba krawędzi M musi być co najmniej N-1 oraz nie większa niż 100.")
    if K <= 0 or K > N or K > 20:
        raise ValueError("Parametr K musi być dodatni, nie większy niż N oraz nie większy niż 20.")


def generate_graph(N, M, seed=42):
    if seed is not None:
        random.seed(seed)

    G_nx = nx.Graph()
    G_nx.add_nodes_from(range(1, N + 1))

    # drzewo 1–2–3–…–N, żeby graf był spójny
    for i in range(1, N):

        G_nx.add_edge(i, i + 1)

    # dokładamy losowe krawędzie do M
    while G_nx.number_of_edges() < M:
        u = random.randint(1, N)
        v = random.randint(1, N)
        if u != v and not G_nx.has_edge(u, v):
            G_nx.add_edge(u, v)

    # konwersja na słownik z wagami
    graph_dict = {str(i): [] for i in range(1, N + 1)}
    for u, v in G_nx.edges():
        w = random.randint(1, 5)
        su, sv = str(u), str(v)
        graph_dict[su].append((sv, w))
        graph_dict[sv].append((su, w))  # graf nieskierowany

    return graph_dict


def dijkstra_stop(graph, s, t):
    import heapq

    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[s] = 0.0

    pq = [(0.0, s)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        if v == t:
            break

        for w, weight in graph[v]:
            nd = d + weight
            if nd < dist[w]:
                dist[w] = nd
                prev[w] = v
                heapq.heappush(pq, (nd, w))

    if dist[t] == float("inf"):
        raise ValueError(f"Brak ścieżki z {s} do {t}.")

    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    return dist[t], path


def solve_museum_tour(graph, start_node, museum_list):
    sorted_museums = sorted(museum_list, key=lambda x: int(x))

    current_node = start_node
    total_time = 0
    full_path = [start_node]

    print("-" * 40)
    print(f"Muzea do odwiedzenia: {sorted_museums}")

    for museum in sorted_museums:
        if current_node == museum:
            print(f" -> Jestem już w muzeum {museum} (czas: 0)")
            continue

        dist, segment = dijkstra_stop(graph, current_node, museum)
        total_time += dist
        full_path.extend(segment[1:])
        print(f" -> Z {current_node} do {museum}: czas {dist}, trasa {segment}")
        current_node = museum

    # powrót na dworzec (1)
    if current_node != start_node:
        dist, segment = dijkstra_stop(graph, current_node, start_node)
        total_time += dist
        full_path.extend(segment[1:])
        print(f" -> POWRÓT z {current_node} do {start_node}: czas {dist}, trasa {segment}")

    return total_time, full_path


def visualize_museum_graph(graph_dict, museum_ids):
    G = nx.Graph()
    for u in graph_dict:
        for v, w in graph_dict[u]:
            G.add_edge(u, v, weight=w)

    node_colors = []
    for node in G.nodes():
        node_str = str(node)
        if node_str == "1":
            node_colors.append("green")   # dworzec
        elif node_str in museum_ids:
            node_colors.append("pink")    # muzea
        else:
            node_colors.append("white")   # inne przystanki

    plt.figure(figsize=(12, 8))

    try:
        pos = nx.kamada_kawai_layout(G)
    except Exception:
        pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, edgecolors="black", node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(f"Plan Bitowic: {len(G.nodes())} przystanków, {len(museum_ids)} muzeów", fontsize=15)
    plt.axis("off")
    plt.show()


def simulation(N, M, K, manual_graph=None, manual_museums=None):
    # 1. Ustalanie które przystanki są muzeami
    if manual_museums:
        museum_ids = manual_museums
    else:
        # Losujemy K muzeów spośród przystanków
        possible_stops = list(range(1, N + 1))
        random_museum_ints = random.sample(possible_stops, K)
        museum_ids = [str(m) for m in random_museum_ints]

    # 2. Generowanie lub użycie podanego grafu
    if manual_graph:
        graph = manual_graph
    else:
        graph = generate_graph(N, M, seed=None)

    # 3. Rozwiązanie problemu
    start_node = "1"
    total_time, full_path = solve_museum_tour(graph, start_node, museum_ids)

    # 4. Wyjście
    print("\n" + "=" * 40)
    print("WYNIKI SYMULACJI")
    print("=" * 40)
    print("-" * 40)
    print(f"Całkowity czas przejazdu: {total_time}")
    print(f"Pełna ścieżka sekwencyjna: {full_path}")
    print("=" * 40)

    # 5. Wizualizacja
    print("\nOtwieranie okna z wykresem...")
    visualize_museum_graph(graph, museum_ids)
    
def pobierz_liczbe(komunikat, min_val, max_val):
    while True:
        try:
            val_str = input(komunikat)
            val = int(val_str)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Błąd: Liczba musi być z zakresu od {min_val} do {max_val}.")
        except ValueError:
            print("Błąd: To nie jest liczba całkowita. Spróbuj ponownie.")

def main():
    print("Projekt 12: Zwiedzanie Muzeów (Bitowice)")
    print("-" * 60)
    print("Tematyka projektu")
    print("Program pomaga Bajtazarowi zaplanować najszybszą trasę wycieczki po muzeach.")
    print("Zasady:")
    print("1. Początek i koniec trasy są zawsze na Dworcu autobusowym - przystanku nr 1.")
    print("2. Bajtazar musi odwiedzić K muzeów rozmieszczonych w mieście.")
    print("3. Muzea są zwiedzane w kolejności rosnącej")
    print("   numerów przystanków, np. najpierw przystanek 3, potem 7, potem 12.")
    print("4. Program oblicza minimalny czas przejazdu, sumując najkrótsze")
    print("   ścieżki między kolejnymi punktami harmonogramu.")
    print("5. Mamy łączie N ponumerowanych przystanków autobusowych oraz M ścieżek łączących je.")
    print("-" * 60)
    while True:
        print("\n")
        print("1) Wprowadź dane całkowicie ręcznie (graf i muzea)")
        print("2) Wprowadź parametry (N, M, K) ręcznie, graf i muzea losowe")
        print("3) Wygeneruj wszystko losowo")
        print("4) Wyjdź z programu")
        wybor = input("Wprowadź z klawiatury jedną z opcji 1-4: ").strip()

        if wybor == "1":
            print("\n--- Tryb Ręczny ---")
            
            # 1. Pobieramy N (1-50)
            N = pobierz_liczbe("Podaj liczbę przystanków N (1-50): ", 1, 50)
            
            # 2. Pobieramy M (zależy od N)
            min_edges = N - 1
            M = pobierz_liczbe(f"Podaj liczbę połączeń M (min {min_edges}, max 100): ", min_edges, 100)
            
            # 3. Pobieramy K (zależy od N i limitu 20)
            max_K = min(N, 20)
            K = pobierz_liczbe(f"Podaj liczbę muzeów K (1-{max_K}): ", 1, max_K)
                
            validate_parameters(N, M, K)
            
            # Ręczne wskazywanie muzeów
            print(f"Podaj numery {K} przystanków, gdzie są muzea:")
            manual_museums = []
            while len(manual_museums) < K:
                m = pobierz_liczbe(f"Muzeum nr {len(manual_museums)+1} (nr przystanku): ", 1, N)
                # Dodatkowe sprawdzenie czy już nie dodaliśmy tego muzeum
                if str(m) not in manual_museums:
                    manual_museums.append(str(m))
                else:
                    print("To muzeum już zostało dodane!")

            # Ręczne budowanie grafu
            print("\nDefiniowanie połączeń (format: x y t):")
            print("Gdzie: x, y - numery przystanków, t - czas przejazdu (max 5)")
            manual_graph = {str(i): [] for i in range(1, N + 1)}
            added_edges = 0
            while added_edges < M:
                line = input(f"Krawędź {added_edges+1}/{M}: ").split()
                
                if len(line) != 3:
                    print("Błąd: Wpisz dokładnie 3 liczby oddzielone spacją (x y t).")
                    continue

                try:
                    # Konwersja na int dla sprawdzenia poprawności
                    u_int = int(line[0])
                    v_int = int(line[1])
                    t_int = int(line[2])

                    # 1. Sprawdzenie zakresu przystanków
                    if not (1 <= u_int <= N and 1 <= v_int <= N):
                        print(f"Błąd: Numery przystanków muszą być z zakresu 1-{N}.")
                        continue

                    # 2. Sprawdzenie czy węzły są różne (nie można łączyć przystanku z samym sobą)
                    if u_int == v_int:
                        print("Błąd: Nie można połączyć przystanku z samym sobą.")
                        continue

                    # 3. Sprawdzenie czasu przejazdu
                    if t_int > 5 or t_int < 0:
                        print("Błąd: Czas przejazdu 't' musi być w zakresie 0-5.")
                        continue

                    # 4. Sprawdzenie czy krawędź już istnieje (graf nieskierowany)
                    u_str, v_str = str(u_int), str(v_int)
                    exists = False
                    for neighbor, _ in manual_graph[u_str]:
                        if neighbor == v_str:
                            exists = True
                            break
                    
                    if exists:
                        print(f"Błąd: Połączenie między {u_int} a {v_int} już istnieje.")
                        continue

                    # Dodajemy krawedz jesli wszystko jest dobrze
                    manual_graph[u_str].append((v_str, t_int))
                    manual_graph[v_str].append((u_str, t_int))
                    added_edges += 1

                except ValueError:
                    print("Błąd: Podane wartości muszą być liczbami całkowitymi.")    
                
            try:
                # Tutaj próbujemy obliczyć trasę
                total_time, full_path = solve_museum_tour(manual_graph, "1", manual_museums)
                
            
                print(f"Całkowity czas: {total_time}")
                print(f"Ścieżka: {full_path}")
                visualize_museum_graph(manual_graph, manual_museums)
            
            except ValueError as e:
                # Jeśli graf jest niespójny (brak trasy)
                print("Błąd danych: otrzymany graf jest niespójny")
                print(f"Przyczyna techniczna: {e}")
                input("\nNaciśnij Enter, aby wrócić do MENU GŁÓWNEGO i spróbować ponownie...")
            
        elif wybor == "2":
            N = pobierz_liczbe("Podaj liczbę przystanków N (1-50): ", 1, 50)
            
            min_edges = N - 1
            M = pobierz_liczbe(f"Podaj liczbę połączeń M (min {min_edges}, max 100): ", min_edges, 100)
            
            max_K = min(N, 20)
            K = pobierz_liczbe(f"Podaj liczbę muzeów K (1-{max_K}): ", 1, max_K)
            simulation(N, M, K)
        
        elif wybor == "3":
            N = random.randint(5, 15)
            M = random.randint(N, min(N*(N-1)//2, 30))
            K = random.randint(2, min(N-1, 5))
            print(f"\nWylosowano parametry: N={N}, M={M}, K={K}")
            simulation(N, M, K)
        elif wybor == "4":
            print("Zamknięcie programu")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")
            continue

if __name__ == "__main__":
    main()
