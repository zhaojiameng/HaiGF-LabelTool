import os
import gui_src
env_path = "/home/zzd/anaconda3/envs/hai_ltt_env/lib/python3.8/site-packages/cv2/qt/plugins/platforms"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = env_path
gui_src.main(name='framework')
