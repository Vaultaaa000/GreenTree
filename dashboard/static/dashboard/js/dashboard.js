// 等待DOM完全加载
document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    initDepartmentChart();
    initAttendanceChart();
});

// 初始化部门员工分布图表（饼图）
async function initDepartmentChart() {
    try {
        // 获取数据
        const data = await fetch('/api/dashboard/department-data/')
            .then(response => response.json());

        // 获取canvas元素的上下文
        const ctx = document.getElementById('departmentChart').getContext('2d');

        // 创建饼图
        const departmentChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.department_names,
                datasets: [{
                    data: data.employee_counts,
                    backgroundColor: [
                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
                        '#6f42c1', '#5a5c69', '#2ecc71', '#3498db', '#9b59b6'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const dataset = context.dataset;
                                const total = dataset.data.reduce((prev, curr) => prev + curr, 0);
                                const currentValue = dataset.data[context.dataIndex];
                                const percentage = Math.round((currentValue / total) * 100);
                                return `${context.label}: ${currentValue} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading department chart:', error);
    }
}

// 初始化出勤概览图表（柱状图）- 适用于 Chart.js v3
async function initAttendanceChart() {
    try {
        // 获取数据
        const data = await fetch('/api/dashboard/attendance-data/')
            .then(response => response.json());

        // 获取canvas元素的上下文
        const ctx = document.getElementById('attendanceChart').getContext('2d');

        // 创建柱状图 - 修改配置以匹配图片，适用于 Chart.js v3
        const attendanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.days,
                datasets: [
                    {
                        label: 'Present',
                        data: data.present_counts,
                        backgroundColor: '#36b9cc',  // 绿色
                        borderWidth: 0,
                        order: 1  // 顺序: 显示在底部
                    },
                    {
                        label: 'Late',
                        data: data.late_counts,
                        backgroundColor: '#f6c23e',  // 黄色
                        borderWidth: 0,
                        order: 2  // 顺序: 显示在中间
                    },
                    {
                        label: 'Absent',
                        data: data.absent_counts,
                        backgroundColor: '#e74a3b',  // 红色
                        borderWidth: 0,
                        order: 3  // 顺序: 显示在顶部
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: true,  // 启用堆叠 - Chart.js v3 语法
                        grid: {
                            display: true,
                            color: "rgba(0, 0, 0, 0.1)"
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        stacked: true,  // 启用堆叠 - Chart.js v3 语法
                        grid: {
                            display: true,
                            color: "rgba(0, 0, 0, 0.1)"
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 5
                        },
                        title: {
                            display: true,
                            text: 'Number of Employees'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        align: 'center',
                        labels: {
                            boxWidth: 12,
                            usePointStyle: false
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading attendance chart:', error);
    }
}