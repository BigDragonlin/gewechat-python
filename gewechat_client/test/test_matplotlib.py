import unittest
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

class TestMatplotlib(unittest.TestCase):
    def setUp(self):
        # 假设有一年的运动数据，每天的运动次数
        np.random.seed(0)
        self.activity_data = np.random.randint(0, 11, size=365)

        # 创建一个7天 * 53周的网格
        days_in_week = 7
        weeks = 53
        self.activity_grid = np.zeros((days_in_week, weeks), dtype=int)

        # 将实际数据填充到网格中
        for i in range(365):
            day_of_week = i % 7
            week_number = i // 7
            self.activity_grid[day_of_week, week_number] = self.activity_data[i]

    def test_plot_creation(self):
        # 创建图形和子图
        fig, ax = plt.subplots(figsize=(15, 10))

        # 绘制运动活跃图
        cmap = plt.cm.get_cmap('Greens')  # 使用绿色渐变色
        cax = ax.imshow(self.activity_grid, cmap=cmap, aspect='auto')

        # 设置x轴和y轴标签
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax.set_xticks(np.linspace(0, 52, 13)[:-1])  # 12个等间距的刻度
        ax.set_xticklabels(months, rotation=45, ha='right')
        ax.set_yticks(np.arange(7))
        ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

        # 添加颜色条
        cbar = fig.colorbar(cax)
        cbar.set_label('Number of Activities')

        # 设置标题和标签
        ax.set_title('Annual Activity Chart for 2025')
        ax.set_xlabel('Month')
        ax.set_ylabel('Day of the Week')

        # 检查图形是否正确创建
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertIsNotNone(cax)
        self.assertIsNotNone(cbar)

        # 保存图形到字节流以验证
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        self.assertGreater(len(buf.getvalue()), 0)

        # 关闭图形以释放内存
        plt.close(fig)

if __name__ == '__main__':
    unittest.main()