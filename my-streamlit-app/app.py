Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 页面配置
st.set_page_config(
    page_title="数据可视化仪表板",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 交互式数据可视化仪表板")
st.markdown("---")

# 侧边栏：数据上传和控制
with st.sidebar:
    st.header("⚙️ 控制面板")
    
    # 数据源选择
    data_source = st.radio(
        "选择数据源",
        ["示例数据", "上传CSV文件", "使用演示数据"]
    )
    
    # 文件上传
    if data_source == "上传CSV文件":
        uploaded_file = st.file_uploader("选择CSV文件", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("文件上传成功！")
        else:
            st.info("请上传CSV文件")
            df = None
    elif data_source == "示例数据":
        # 生成示例数据
        np.random.seed(42)
        df = pd.DataFrame({
            '日期': pd.date_range('2024-01-01', periods=100, freq='D'),
            '销售额': np.random.randint(1000, 5000, 100),
            '利润': np.random.randint(100, 1000, 100),
            '类别': np.random.choice(['A', 'B', 'C', 'D'], 100),
            '区域': np.random.choice(['北区', '南区', '东区', '西区'], 100),
            '评分': np.random.uniform(1, 5, 100)
        })
    else:  # 使用演示数据
        # 加载iris数据集
        df = sns.load_dataset('iris')

# 如果df存在，进行可视化
if df is not None:
    # 显示数据概览
    with st.expander("📋 数据概览", expanded=False):
        col1, col2, col3 = st.columns(3)
        col1.metric("行数", df.shape[0])
        col2.metric("列数", df.shape[1])
        col3.metric("缺失值", df.isnull().sum().sum())
        
        st.dataframe(df.head(10))
        st.write("### 数据统计描述")
        st.dataframe(df.describe())
    
    st.markdown("---")
    
    # 主区域：图表展示
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 折线图 - 趋势分析")
        # 选择数值列
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 1:
            y_axis = st.selectbox("选择Y轴", numeric_cols, key="line_y")
            x_axis = st.selectbox("选择X轴", df.columns, key="line_x")
            
            # 使用Plotly创建交互式折线图
            fig_line = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} 趋势")
            st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.subheader("📊 柱状图 - 类别对比")
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols) > 0 and len(numeric_cols) > 0:
            cat_axis = st.selectbox("选择类别", cat_cols, key="bar_cat")
            num_axis = st.selectbox("选择数值", numeric_cols, key="bar_num")
            
            # 聚合数据
            bar_data = df.groupby(cat_axis)[num_axis].mean().reset_index()
            fig_bar = px.bar(bar_data, x=cat_axis, y=num_axis, 
                           title=f"各{cat_axis}平均{num_axis}")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # 第二行图表
    col3, col4 = st.columns(2)
    
    with col3:
...         st.subheader("🥧 饼图 - 占比分析")
...         if len(cat_cols) > 0:
...             pie_col = st.selectbox("选择分类", cat_cols, key="pie_col")
...             pie_data = df[pie_col].value_counts().reset_index()
...             pie_data.columns = [pie_col, 'count']
...             fig_pie = px.pie(pie_data, values='count', names=pie_col, 
...                            title=f"{pie_col}分布")
...             st.plotly_chart(fig_pie, use_container_width=True)
...     
...     with col4:
...         st.subheader("🔍 散点图 - 相关性分析")
...         if len(numeric_cols) >= 2:
...             x_scatter = st.selectbox("X轴", numeric_cols, key="scatter_x")
...             y_scatter = st.selectbox("Y轴", numeric_cols, key="scatter_y")
...             
...             # 如果有分类列，可以用颜色区分
...             color_col = None
...             if len(cat_cols) > 0:
...                 color_col = st.selectbox("颜色分组(可选)", ["无"] + cat_cols, key="scatter_color")
...                 if color_col == "无":
...                     color_col = None
...             
...             fig_scatter = px.scatter(df, x=x_scatter, y=y_scatter, color=color_col,
...                                    title=f"{x_scatter} vs {y_scatter}")
...             st.plotly_chart(fig_scatter, use_container_width=True)
...     
...     # 热力图（相关性矩阵）
...     if len(numeric_cols) > 1:
...         st.subheader("🔥 相关性热力图")
...         corr_matrix = df[numeric_cols].corr()
...         fig_heatmap = px.imshow(corr_matrix, 
...                                text_auto=True, 
...                                aspect="auto",
...                                color_continuous_scale='RdBu_r',
...                                title="数值特征相关性矩阵")
...         st.plotly_chart(fig_heatmap, use_container_width=True)
... 
... else:
    st.info("请在左侧边栏上传数据文件或选择数据源")

# 页脚
st.markdown("---")
