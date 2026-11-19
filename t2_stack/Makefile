help:
	@echo \
	"init: once at start, use instead of uv sync \n\
	shell: enter T2 shell, follow booster manual terminal access first \n\
	uv_full_sync: clean .venv and sync using --system-site-packages (required for ROS2)"


init: chmod_scripts uv_full_sync
	
chmod_scripts:
	chmod +x scripts/shell.sh
	chmod +x scripts/uv_full_sync.sh

uv_full_sync:
	./scripts/uv_full_sync.sh

shell:
	./scripts/shell.sh

