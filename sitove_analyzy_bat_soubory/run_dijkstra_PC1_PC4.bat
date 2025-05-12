@echo off
echo === Spoustim Dijkstra z PC1 do PC4 ===
docker run --rm -v "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt:/app" nosleepxd/sitovy-projekt python main.py --dijkstra PC1 PC4
echo === Oteviram obrazek ===
start "" "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt\network_dijkstra_PC1_PC4.png"
pause
