@echo off
echo === Spoustim DFS z R1 ===
docker run --rm -v "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt:/app" nosleepxd/sitovy-projekt python main.py --dfs R1
echo === Oteviram obrazek ===
start  "C:\Users\lolik\OneDrive\Desktop\programky\sitovy-projekt\network_dfs_R1.png"
pause