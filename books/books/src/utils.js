// 工具函数库

export function get (url, data, header) {
  return request(url, 'GET', data, header)
}

export function post (url, data, header) {
  return request(url, 'POST', data, header)
}

function request (url, method, data, header) {
  return new Promise((resolve, reject) => {
    wx.request({
      data,
      method,
      header,
      url: url,
      success: function (res) {
        if (res.data.error_code === 0) {
          resolve(res.data.data)
        } else {
          return false
        }
      }
    })
  })
}

export function showSuccess (text, icon = 'none') {
  wx.showToast({
    title: text,
    icon: icon
  })
}

export function showModalLogin () {
  wx.showModal({
    title: '提示',
    content: '你还未登录, 请先登录',
    success: function (res) {
      if (res.confirm) {
        console.log('用户点击确定')
        wx.switchTab({
          url: '/pages/me/main'
        })
      } else if (res.cancel) {
        console.log('用户点击取消')
      }
    }
  })
}

export function showLoadings () {
  wx.showLoading({
    title: '加载中'
  })
  setTimeout(function () {
    wx.hideLoading()
  }, 800)
}
