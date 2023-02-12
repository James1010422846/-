# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import finance as fi
print(fi.bankdate)
import matplotlib.pyplot as plt
import decimalpy as dp
import finance as fn

ns = fn.yieldcurves.NelsonSiegel(1, 1, 1, 1)
tau_list = dp.Vector([1, 4])
legend_list = [r"$\beta_0-factor$ is the same for both $\tau$'s"]
xdata = dp.Vector(range(61)) * 0.5
b0_factor = dp.Vector(61, 1)

plt.plot(xdata, b0_factor)
for tau in tau_list:
    ns.scale = 1 / tau
    plt.plot(
        xdata, ns.Slope(xdata),
        xdata, ns.Curvature(xdata)
    )
    for fac in (1,2):
        legend_list.append(r'$\beta_%s-factor, \tau = %s$' % (fac, tau))

tau_in_title = ' and '.join([r'$\tau = %s$' % x for x in tau_list])
plt.title(r'Showing Nelson Siegel curves for %s' % tau_in_title)
plt.xlabel('time (years)')
plt.grid(True)
plt.ylim(-0.5,1.5)
plt.legend(legend_list)
plt.show()
def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
