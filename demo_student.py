import streamlit as st
import streamlit.components.v1 as components
import random
import base64
import json
from pathlib import Path

# ---------------------------------
# 0. Cấu hình đường dẫn (Hệ thống - Đừng sửa phần này)
# ---------------------------------
ROOT_DIR = Path(__file__).parent

def get_asset_path(relative_path):
    return ROOT_DIR / relative_path

def file_to_data_url(path_obj):
    if not path_obj.exists():
        return ""
    encoded = base64.b64encode(path_obj.read_bytes()).decode("utf-8")
    return "data:audio/mpeg;base64," + encoded if path_obj.suffix == ".mp3" else "data:image/png;base64," + encoded

# ---------------------------------
# 1. Cấu hình trang & Assets
# ---------------------------------
st.set_page_config(
    page_title="Học Python: Oẳn Tù Tì (Bài tập)",
    page_icon="🐢",
    layout="centered"
)

SOUNDS = {
    "bg": file_to_data_url(get_asset_path("music/game_theme.mp3")),
    "click": file_to_data_url(get_asset_path("music/game_click.mp3")),
    "win": file_to_data_url(get_asset_path("music/game_winner.mp3")),
    "lose": file_to_data_url(get_asset_path("music/game_over.mp3"))
}

IMAGE_PATHS = {
    "Búa": "assets/rock.png",
    "Bao": "assets/paper.png",
    "Kéo": "assets/scissors.png"
}

# ---------------------------------
# 2. Khởi tạo bộ nhớ (Session State)
# ---------------------------------
# TODO: Thử thách 1 - Khởi tạo score_player và score_computer bằng 0 nếù chưa có
if "player_score" not in st.session_state:
    ### BẮT ĐẦU CODE CỦA EM ###
    pass # Thay dòng này bằng code của em (Gợi ý: st.session_state.player_score = 0)
    ### KẾT THÚC CODE CỦA EM ###

if "computer_score" not in st.session_state:
    ### BẮT ĐẦU CODE CỦA EM ###
    pass
    ### KẾT THÚC CODE CỦA EM ###

if "result_text" not in st.session_state:
    st.session_state.result_text = "Hãy chọn một quân bài!"
if "sound_trigger" not in st.session_state:
    st.session_state.sound_trigger = 0
if "last_event" not in st.session_state:
    st.session_state.last_event = ""
if "player_choice" not in st.session_state:
    st.session_state.player_choice = None
if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = None

# ---------------------------------
# 3. Audio Engine (Đừng sửa phần này)
# ---------------------------------
def render_audio():
    payload = json.dumps({
        "sounds": SOUNDS,
        "trigger": st.session_state.sound_trigger,
        "event": st.session_state.last_event
    })
    html_code = f"""
    <script>
    const data = {payload};
    function playSound(url) {{ if (!url) return; new Audio(url).play().catch(() => {{}}); }}
    if (!window.bgMusic) {{
        window.bgMusic = new Audio(data.sounds.bg);
        window.bgMusic.loop = true; window.bgMusic.volume = 0.3;
        window.bgMusic.play().catch(() => {{}});
    }}
    const lastTrigger = window.localStorage.getItem("rps_trigger");
    if (String(data.trigger) !== lastTrigger && data.event) {{
        window.localStorage.setItem("rps_trigger", data.trigger);
        if (data.event === "win") playSound(data.sounds.win);
        else if (data.event === "lose") playSound(data.sounds.lose);
        else playSound(data.sounds.click);
    }}
    </script>
    """
    components.html(html_code, height=0)

# ---------------------------------
# 4. Logic xử lý game (Phần quan trọng nhất)
# ---------------------------------
choices = ["Kéo", "Búa", "Bao"]

def play(player_choice):
    st.session_state.player_choice = player_choice
    
    # TODO: Thử thách 2 - Máy tính chọn bài ngẫu nhiên từ danh sách 'choices'
    ### BẮT ĐẦU CODE CỦA EM ###
    st.session_state.computer_choice = "Búa" # Thay "Búa" bằng hàm chọn ngẫu nhiên
    ### KẾT THÚC CODE CỦA EM ###
    
    p = st.session_state.player_choice
    c = st.session_state.computer_choice

    # TODO: Thử thách 3 - Quyết định Thắng, Thua, Hòa bằng if/elif/else
    if p == c:
        st.session_state.result_text = "Hòa rồi!"
        st.session_state.last_event = "click"
    
    ### BẮT ĐẦU CODE CỦA EM (Viết logic thắng cho Người chơi) ###
    
    # Gợi ý: elif (player chọn Búa và computer chọn Kéo) hoặc ...
    
    ### KẾT THÚC CODE CỦA EM ###

    else:
        st.session_state.result_text = "Máy Thắng! 🤖"
        # TODO: Thử thách 4 - Tăng điểm cho Máy tính
        ### BẮT ĐẦU CODE CỦA EM ###
        pass 
        ### KẾT THÚC CODE CỦA EM ###
        st.session_state.last_event = "lose"
    
    st.session_state.sound_trigger += 1

# ---------------------------------
# 5. Giao diện người dùng (UI)
# ---------------------------------
render_audio()

st.title("🐢 Game Oẳn Tù Tì (Phiên bản thực hành)")
st.write("Em hãy điền code vào các phần TODO để làm game hoạt động nhé!")

# Hiển thị điểm số
col_a, col_b = st.columns(2)
col_a.metric("Bạn", st.session_state.player_score)
col_b.metric("Máy tính", st.session_state.computer_score)

st.divider()

# Hiển thị quân bài
if st.session_state.player_choice:
    disp1, disp2 = st.columns(2)
    with disp1:
        st.write("### Bạn chọn:")
        st.image(str(get_asset_path(IMAGE_PATHS[st.session_state.player_choice])), width=150)
    with disp2:
        st.write("### Máy chọn:")
        st.image(str(get_asset_path(IMAGE_PATHS[st.session_state.computer_choice])), width=150)

st.divider()

# Các nút chọn
st.subheader("Bấm nút để chơi:")
c1, c2, c3 = st.columns(3)

# TODO: Thử thách 5 - Gọi hàm play() tương ứng khi bấm mỗi nút
if c1.button("🪨 Búa", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    pass
    ### KẾT THÚC CODE CỦA EM ###

if c2.button("📄 Bao", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    pass
    ### KẾT THÚC CODE CỦA EM ###

if c3.button("✂️ Kéo", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    pass
    ### KẾT THÚC CODE CỦA EM ###

st.divider()
st.markdown(f"<h2 style='text-align: center;'>{st.session_state.result_text}</h2>", unsafe_allow_html=True)

if st.button("Reset Game"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.result_text = "Hãy chọn một quân bài!"
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.rerun()
