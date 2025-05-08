// dashboard/static/dashboard/js/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
   // Initialize department employee distribution chart
   initDepartmentChart();

   // Initialize monthly attendance chart
   initAttendanceChart();
});

function initDepartmentChart() {
   fetch('/api/department-data/')
       .then(response => response.json())
       .then(data => {
           const ctx = document.getElementById('departmentChart').getContext('2d');

           new Chart(ctx, {
               type: 'pie',
               data: {
                   labels: data.department_names,
                   datasets: [{
                       data: data.employee_counts,
                       backgroundColor: [
                           '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'
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
                               boxWidth: 12
                           }
                       },
                       tooltip: {
                           callbacks: {
                               label: function(context) {
                                   const label = context.label || '';
                                   const value = context.raw || 0;
                                   const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                   const percentage = Math.round((value / total) * 100);
                                   return `${label}: ${value} employees (${percentage}%)`;
                               }
                           }
                       }
                   }
               }
           });
       })
       .catch(error => console.error('Error fetching department data:', error));
}

function initAttendanceChart() {
   fetch('/api/attendance-data/')
       .then(response => response.json())
       .then(data => {
           const ctx = document.getElementById('attendanceChart').getContext('2d');

           new Chart(ctx, {
               type: 'bar',
               data: {
                   labels: data.days,
                   datasets: [
                       {
                           label: 'Present',
                           data: data.present_counts,
                           backgroundColor: '#1cc88a',
                           borderColor: '#1cc88a',
                           borderWidth: 1
                       },
                       {
                           label: 'Late',
                           data: data.late_counts,
                           backgroundColor: '#f6c23e',
                           borderColor: '#f6c23e',
                           borderWidth: 1
                       },
                       {
                           label: 'Absent',
                           data: data.absent_counts,
                           backgroundColor: '#e74a3b',
                           borderColor: '#e74a3b',
                           borderWidth: 1
                       }
                   ]
               },
               options: {
                   responsive: true,
                   maintainAspectRatio: false,
                   scales: {
                       x: {
                           title: {
                               display: true,
                               text: 'Date'
                           },
                           stacked: true
                       },
                       y: {
                           title: {
                               display: true,
                               text: 'Number of Employees'
                           },
                           stacked: true
                       }
                   },
                   plugins: {
                       legend: {
                           position: 'top'
                       }
                   }
               }
           });
       })
       .catch(error => console.error('Error fetching attendance data:', error));
}