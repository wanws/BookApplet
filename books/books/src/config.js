// 配置文件项
const host = 'http://127.0.0.1:5000'

// 个人中心图标
const MeImge = {
  browsing_history: '../../../static/image/browsing-history.png',
  qiandao: '../../../static/image/qiandao.png',
  jingyan: '../../../static/image/jingyan.png',
  message: '../../../static/image/message.png',
  invitation: '../../../static/image/invitation.png',
  my_bookcase: '../../../static/image/my-books.png'
}
const config = {
  host,
  MeImge,
  loginUrl: `${host}/v1/user/login`,
  UserindexUrl: `${host}/v1/provide/get`,
  indexUrl: `${host}/v1/provide/get_index`,
  detailUrl: `${host}/v1/provid/get_book_info`,
  sectionUrl: `${host}/v1/provid/get_book_section`,
  postBookUrl: `${host}/v1/provid/post_book`,
  contentUrl: `${host}/v1/book/chapter/parse`,
  getSubQueryUrl: `${host}/v1/book/search_sub`,
  getSearchQueryUrl: `${host}/v1/book/search`,
  getSearchHptWordsUrl: `${host}/v1/book/hot_words`,
  getBookTypeUrl: `${host}/v1/book/statistics`,
  getBookCategoriesUrl: `${host}/v1/book/by-categories`
}

export default config
