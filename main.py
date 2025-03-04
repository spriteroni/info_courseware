import gradio as gr

import runpy
import dbsave


def add_page():
    with gr.Row():
        name_input = gr.Textbox(label="姓名")
        age_input = gr.Number(label="年龄")
    save_button = gr.Button("保存")
    output = gr.Textbox(label="结果")
    # 绑定按钮事件
    save_button.click(fn=dbsave.save_to_db, inputs=[name_input, age_input], outputs=output)


def list_page():
    name_input = gr.Textbox(label="输入姓名")
    query_button = gr.Button("查询")
    delete_button = gr.Button("删除")
    query_output = gr.Dataframe(
        headers=["ID", "姓名", "年龄"],
        value=dbsave.query_db(""),
        col_count=3)
        #interactive=True)
    query_button.click(fn=dbsave.query_db, inputs=name_input, outputs=query_output)
    delete_button.click(fn=dbsave.delete_db, inputs=name_input, outputs=query_output)


iface_add = gr.Interface(fn=add_page, inputs=[], outputs="text", title="新增")
iface_list = gr.Interface(fn=list_page, inputs=[], outputs="text", title="列表")

with gr.Blocks() as page:
    with gr.Tab("新增"):
        gr.Markdown(add_page())
    with gr.Tab("列表"):
        gr.Markdown(list_page())
        dbsave.query_db("")

# with gr.Blocks() as page:
#     with gr.Row():
#         btn_page1 = gr.Button("Go to Page 1")
#         btn_page2 = gr.Button("Go to Page 2")
#
#     btn_page1.click(lambda: iface_add.launch(), inputs=[], outputs=[])
#     btn_page2.click(lambda: iface_list.launch(), inputs=[], outputs=[])

# demo = gr.Interface(  # “interface”界面（中文）；gr.Interface 是 Gradio 库中的一个类，demo是gr.Interface这个类的实例；
#     fn=greet,
#     inputs=["text", "slider"],  # "slider"滑块（中文）；
#     outputs=["text"],
# )
# fn、inputs 和 outputs 是用于定义 Gradio 界面行为和组件的参数；
# 调用 Gradio 接口对象 demo 的方法；用于启动交互式界面；


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    runpy.run_path('initdb.py')
    page.launch()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
