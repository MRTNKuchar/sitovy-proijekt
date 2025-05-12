@echo off
echo === Spoustim BFS z R1 ===
docker run --rm -v "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt:/app" nosleepxd/sitovy-projekt python main.py --bfs R1
echo === Oteviram obrazek ===
start "" "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt\network_bfs_R1.png"
pause
