

var myChart = echarts.init(document.getElementById('chart'));

var schema = [
    {name: 'ID', index: 0},
    {name: 'Concentration', index: 1},
    {name: 'Group', index: 2},
    {name: 'IS', index: 3},
    {name: 'Acetate', index: 4},
    {name: 'Propionate', index: 5},
    {name: 'Isobutyrate', index: 6},
    {name: 'Butyrate', index: 7}
];

var fieldIndices = schema.reduce(function(obj, item) {
    obj[item.name] = item.index;
    return obj;
}, {});

var groupCategories = [];
var groupColors = [];
var data;

$.get('../media/jsonfile/data.json', function (originData) {
    data = normalizeData(originData).slice(0, 1000);
    myChart.setOption(getOption(data));
});

myChart.getZr().configLayer(1, {
    motionBlur: 0.5
});

function normalizeData(originData) {
    var groupMap = {};
    originData.forEach(function (row) {
    var groupName = row[indices.group];
    if (!groupMap.hasOwnProperty(groupName)) {
        groupMap[groupName] = 1;
    }
    });

    originData.forEach(function (row) {
        row.forEach(function (item, index) {
        if (index !== indices.name
            && index !== indices.group
            && index !== indices.id
        ) {
        // Convert null to zero, as all of them under unit "g".
            row[index] = parseFloat(item) || 0;
            }
        });
    });

    for (var groupName in groupMap) {
        if (groupMap.hasOwnProperty(groupName)) {
            groupCategories.push(groupName);
        }
    }
    var hStep = Math.round(300 / (groupCategories.length - 1));
    for (var i = 0; i < groupCategories.length; i++) {
        groupColors.push(echarts.color.modifyHSL('#5A94DF', hStep * i));
    }

    return originData;
}

function getOption(data) {
    return {
        backgroundColor: '#2c343c',
        tooltip: {
            padding: 10,
            backgroundColor: '#222',
            borderColor: '#777',
            borderWidth: 1
        },
        xAxis: {
            name: 'ID',
            splitLine: {show: false},
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#fff'
                }
            },
            axisTick: {
                lineStyle: {
                    color: '#fff'
                }
            }
        },
        yAxis: {
            name: 'Concentration',
            splitLine: {show: false},
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#fff'
                }
            },
            axisTick: {
                lineStyle: {
                    color: '#fff'
                }
            }
        },
        visualMap: [{
            show: false,
            type: 'piecewise',
            categories: groupCatefories,
            dimension: 2,
            inRange: {
                color: groupColors
            },
            outOfRange: {
                color: ['#ccc']
            },
            top: 20,
            textStyle: {
                color: '#fff'
            },
            realtime: false
        }, {
            show: false,
            dimension: 3,
            max: 1000,
            inRange: {
                colorLightness: [0.15, 0.6]
            }
        }],
        series: [
            {
                zlevel: 1,
                name: 'concentration',
                type: 'scatter',
                data: data.map(function (item, idx) {
                    return [item[2], item[3], item[1], idx];
                }),
                animationThreshold: 5000,
                progressiveThreshold: 5000
            }
        ],
        animationEasingUpdate: 'cubicInOut',
        animationDurationUpdate: 2000
    };
}

var fieldNames = schema.map(function (item) {
    return item.name;
}).slice(2);

myChart.config = {
    xAxis: 'ID',
    yAxis: 'Concentration',
    onChange: function() {
        if (data) {
            myChart.setOption( {
                xAxis: {
                    name: app.config.xAxis
                },
                yAxis: {
                    name: app.config.yAxis
                },
                series: {
                    data: data.map(function (item, idx) {
                        return [
                            item[fieldIndices[app.config.xAxis]],
                            item[fieldIndices[app.config.yAxis]],
                            item[1],
                            idx
                        ];
                    })
                }
            });
        }
    }
};

myChart.configParameters = {
    xAxis: {
        options: fieldNames
    },
    yAxis: {
        options: fieldNames
    },
};


