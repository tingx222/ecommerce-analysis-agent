from langchain_core.tools import tool

from sales_service import calculate_sales_summary


#将普通函数包装成带名称、说明和参数定义的工具
@tool
#->dict 声明函数返回一个字典
def get_sales_summary() -> dict:
    """获取全部模拟订单中已支付订单的数量和销售额，金额单位为人民币元。

    不支持按日期、商品或地区筛选，取消订单不计入。
    """
    return calculate_sales_summary()