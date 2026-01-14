import streamlit as st
import requests
import re

# --- 页面配置 ---
st.set_page_config(page_title="表情包搜索", layout="wide", page_icon="🤪")

# --- CSS 样式 ---
st.markdown("""
<style>
    div[data-testid="column"] img {
        border-radius: 8px;
        transition: transform 0.3s ease;
    }
    div[data-testid="column"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# --- 核心逻辑 ---
@st.cache_data(ttl=3600)
def load_bqb_data():
    """
    加载并清洗数据
    """
    # 尝试使用更稳定的 rawgit 源，或者回退到 jsDelivr
    url = "https://cdn.jsdelivr.net/gh/zhaoolee/ChineseBQB@master/chinesebqb_github.json"
    
    try:
        response = requests.get(url, timeout=15) # 增加超时时间
        if response.status_code == 200:
            raw_data = response.json()
            
            # --- 【关键修复】数据清洗 ---
            # 无论远端返回的是 列表(List) 还是 字典(Dict)，都统一转为 List
            if isinstance(raw_data, list):
                return raw_data
            elif isinstance(raw_data, dict):
                # 如果是字典，可能是 {"data": [...]} 或者 {"filename": "url"} 格式
                # 尝试提取 values 或者 keys
                if "data" in raw_data and isinstance(raw_data["data"], list):
                    return raw_data["data"]
                else:
                    # 假设它是 {key: item} 的映射，直接取 values
                    return list(raw_data.values())
            return []
        else:
            return []
    except Exception as e:
        st.error(f"网络请求异常: {e}")
        return []

def parse_item(item):
    """
    解析单条数据
    """
    base_cdn = "https://cdn.jsdelivr.net/gh/zhaoolee/ChineseBQB@master/"
    
    # 1. 字符串格式处理
    if isinstance(item, str):
        parts = item.split('/')
        if len(parts) >= 2:
            category = parts[0]
            name = parts[-1]
        else:
            category = "其他"
            name = item
            
        url = item if item.startswith('http') else f"{base_cdn}{item}"
        return {"name": name, "category": category, "url": url}
        
    # 2. 字典格式处理
    elif isinstance(item, dict):
        url = item.get('url', '')
        if url and not url.startswith('http'):
            url = f"{base_cdn}{url}"
            
        return {
            "name": item.get('name', ''),
            "category": item.get('category', '未分类'),
            "url": url
        }
    return None

def search_bqb(data, keyword):
    results = []
    keyword = keyword.lower()
    
    # 使用 for item in data 直接遍历，不使用下标，防止 KeyError
    for raw_item in data:
        item = parse_item(raw_item)
        if not item: continue
        
        # 模糊匹配
        if keyword in item['name'].lower() or keyword in item['category'].lower():
            results.append(item)
            
    return results

# ================= 界面布局 =================

st.title("🤪 表情包搜索")
st.caption("数据源：ChineseBQB")

# 加载数据
with st.spinner("正在连接 GitHub 仓库..."):
    bqb_data = load_bqb_data()

if bqb_data:
    # --- 侧边栏 ---
    # 【修复】不再使用下标访问，改为直接遍历切片
    # 取前 2000 个数据进行分类提取
    sample_data = bqb_data[:2000] 
    all_categories = set()
    
    for raw_item in sample_data:
        # 这里之前报错，现在因为 sample_data 肯定是 list，且我们用 item 遍历，所以安全了
        item = parse_item(raw_item)
        if item and item.get('category'):
            all_categories.add(item['category'])
            
    with st.sidebar:
        st.success(f"📚 索引加载成功！")
        st.metric("表情包总数", len(bqb_data))
        st.markdown("### 🔥 热门分类")
        st.write(list(all_categories)[:15])

    # --- 搜索区 ---
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("输入关键词", placeholder="搜：猫、熊猫、滑稽...", key="search_input")
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 搜索", type="primary", use_container_width=True)

    if query or search_btn:
        if not query:
            st.warning("请输入关键词")
        else:
            results = search_bqb(bqb_data, query)
            
            if results:
                st.success(f"🎉 找到 {len(results)} 张相关表情！")
                
                # 分页展示防止卡顿
                display_limit = 50
                if len(results) > display_limit:
                    st.info(f"结果较多，为您展示前 {display_limit} 张。")
                    results = results[:display_limit]
                
                cols = st.columns(4)
                for i, item in enumerate(results):
                    col_idx = i % 4
                    with cols[col_idx]:
                        st.image(item['url'], use_container_width=True)
                        clean_name = re.sub(r'\.(jpg|png|gif)$', '', item['name'], flags=re.I)
                        st.caption(f"{clean_name}")
                        st.markdown(f"[⬇️ 原图链接]({item['url']})")
            else:
                st.warning("🤔 没搜到... 试试侧边栏里的分类名？")
    else:
        st.info("👈 试试搜索 'Cat' 或 'Dog' ...")
        
else:
    st.error("⚠️ 数据加载失败。可能是网络无法连接 GitHub CDN。")

st.divider()