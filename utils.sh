DM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WO_DIR=/opt/visual
DK_IMG=visual-dev-env

while :
	do
	echo "1. Build image"
	echo "2. Enter container"
	echo "3. Execute container"
	echo "4. Generate visualization"
	echo "5. EXIT"
	echo -n "Choose one option [1 - 5]: "
	read opcion

function build_dev_image () {
	docker build -t "${DK_IMG}" "${DM_DIR}"/Docker/
}

function enter_dev_env () {
	docker run --rm -it -v  "${DM_DIR}":"${WO_DIR}" --network host "${DK_IMG}" /bin/bash
}

function execute () {
	docker run -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 --rm -it -v  "${DM_DIR}":"${WO_DIR}" --network host "${DK_IMG}" /bin/bash "${WO_DIR}"/utils.sh run
}

function generate_visualization () {
    sudo nano ./conf.json
	docker run --rm -it -v  "${DM_DIR}":"${WO_DIR}" --network host "${DK_IMG}" python3 "${WO_DIR}"/visualization.py run
}


case $opcion in
	1)
		build_dev_image
		;;
	2)
		enter_dev_env
		;;
	3)
		execute
		;;
	4)
		generate_visualization
		;;
	5)
		echo "bye";
		exit 1
		;;
esac
done