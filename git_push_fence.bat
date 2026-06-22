@echo off
cd /d C:\Users\shubo\abu_github
git add noahs_gitee\NOAH_FENCE_MAP.py
git reset --soft HEAD~1
git commit -m "[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21
围栏地图：五类拉弯点 + 镜检7问 + quick_mirror
无闭环。"
git push https://github.com/shuboyuan6/-ABU.git main
