import gradio as gr
import runpy
import dbsave
from datetime import date

def zy_guan_li():
    with gr.Row():
        shi_jian = date.today().strftime("%Y-%m-%d")
        pd = dbsave.xs_query_db("")
        options = pd.to_numpy()
        items = []
        for item in options:
            items.append(str(item[0])+"|"+item[1])

        label = gr.Label(value=dbsave.tong_ji(shi_jian))
        hidden_label= gr.Label(value=f"{shi_jian}已提交",visible=False)
        select = gr.Dropdown(choices=items, multiselect=True, label="选择一个姓名")
        cout = gr.Textbox(label="结果")
        cbtn = gr.Button("提交",variant="huggingface")

    with gr.Row():
        with gr.Column(scale=1):
            name_input = gr.Textbox(label="输入姓名")
        with gr.Column(scale=1):
            shi_jian = gr.DateTime(label="输入提交时间", include_time=False,type="string")
        with gr.Column(scale=1):
            with gr.Row():
                query_zy_button = gr.Button("提交查询")
            with gr.Row():
                query_wj_button = gr.Button("未交查询")

    # delete_button = gr.Button("删除")

    query_output = gr.Dataframe(
        headers=["ID", "姓名", "作业是否提交"],
        value=dbsave.zy_query_db("", ""),
        col_count=3)

    cbtn.click(fn=dbsave.zy_save_to_db, inputs=[select, hidden_label, shi_jian], outputs=[cout, label, query_output])
    query_zy_button.click(fn=dbsave.zy_query_db, inputs=[name_input, shi_jian], outputs=query_output)
    query_wj_button.click(fn=dbsave.wj_query_db,inputs=[shi_jian], outputs=query_output)


def xs_guan_li():
    with gr.Row():
        name_input = gr.Textbox(label="输入姓名")
        sbtn = gr.Button("添加")
        qbtn = gr.Button("查询")
    with gr.Row():
        output = gr.Textbox(label="结果")

    query_output = gr.Dataframe(
        headers=["ID", "姓名"],
        value=dbsave.xs_query_db(""),
        col_count=2,
        column_widths=[100,100])

    # 绑定按钮事件
    sbtn.click(fn=dbsave.xs_save_to_db, inputs=name_input, outputs=[output, query_output])
    qbtn.click(fn=dbsave.xs_query_db, inputs=name_input, outputs=query_output)
    # delete_button = gr.Button("删除")
    #
    # delete_button.click(fn=dbsave.delete_db, inputs=name_input, outputs=query_output)


zuo_ye = gr.Interface(lambda name: "Hello " + name, "text", "text")
xue_sheng = gr.Interface(fn=xs_guan_li, inputs=[], outputs="text", title="学生管理")

with gr.Blocks() as page:
    with gr.Tab("作业管理"):
        zy_guan_li()
        dbsave.zy_query_db("", "")
    with gr.Tab("学生管理"):
        xs_guan_li()
        dbsave.xs_query_db("")

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # runpy.run_path('initdb.py')
    page.launch()
