<template>
    <div class="words">
        <nya-container :title="title + ' ' + book">
            <div v-show="!showInfo">
                <div class="toward nya-btn" @click="changeWords">
                    <span>换一批</span>
                </div>
                <table class="nya-table">
                    <tr>
                        <th>单词</th>
                        <th>音标</th>
                        <th>词义</th>
                    </tr>
                    <tr v-for="(item, index) in words" :key="index">
                        <td>{{ item.word }}</td>
                        <td>美：{{item.spellingA}} 英：{{item.spellingE}}</td>
                        <td class="translation">{{ item.translation }}</td>
                    </tr>
                </table>
            </div>
            <!-- <Table stripe :columns="columns" :data="words"></Table> -->
            <div v-show="showInfo" class="show-info">
                <div class="back nya-btn" @click="showInfo = false">
                    <i class="eva eva-arrow-back-outline"></i>
                    <span>返回</span>
                </div>
                <div class="word-area">
                    <div class="back nya-btn" @click="showInfo = false">
                        <i class="eva eva-arrow-forward-outline"></i>
                        <span>下一个</span>
                    </div>
                </div>
            </div>
        </nya-container>
        <nya-container title="公告" icon="volume-down-outline">
              <ul class="nya-list">
                  <li>可以前往 <a href="/userinfo">用户中心</a>修改单词书和每日单词的数量</li>
                  <li>有意见或建议<a href="/comment_board">欢迎反馈</a></li>
              </ul>
        </nya-container>
    </div>
</template>

<script>
import envs from '../env'
const Cookie = process.client ? require("js-cookie") : undefined;

export default {
  middleware: 'authenticated', // 需要登录
  name: 'ShortUrl',
  head() {
      return{
          title: this.title
      }
  },
  data() {
      return {
          title: '背背单词',
          loading: true,
          showInfo: false,
          book:'',
          columns: [
                  {
                      title: '单词',
                      key: 'word'
                  },
                  {
                      title: '词义',
                      key: 'translation'
                  }
              ],
          words: [],
      };
  },
  mounted (){
      this.getWords()
  },
  methods: {
      getWords() {
          this.$store.commit('SET_STORE', {
              key: 'globalLoading',
              value: true
          });
          this.$axios.defaults.auth = {
            username: Cookie.get('auth'),
            password: ''
          }
          this.$axios
              .get(envs.apiUrl + '/words/daily',)
              .then(re => {
                  this.words = re.data.words;
                  this.$store.commit('SET_STORE', {
                      key: 'globalLoading',
                      value: false
                  });
                  this.book = re.data.book
              })
              .catch(err => {
                this.$store.commit('SET_STORE', {
                    key: 'globalLoading',
                    value: false
                });
                if (err.response.status === 401) {
                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: '登录过期，请重新登录',
                    timer: 3000,
                  });
                  this.$router.push("/login")
                }
                else {
                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: err,
                    timer: 3000,
                  });
                }
              });
          this.loading = false;
      },
      changeWords(){
          this.$store.commit('SET_STORE', {
              key: 'globalLoading',
              value: true
          });
          this.$axios.defaults.auth = {
            username: Cookie.get('auth'),
            password: ''
          }
          this.$axios
              .get(envs.apiUrl + '/words/daily?refresh=1',)
              .then(re => {
                  this.words = re.data.words;
                  this.$store.commit('SET_STORE', {
                      key: 'globalLoading',
                      value: false
                  });
                  this.book = re.data.book
              })
              .catch(err => {
                console.log(err)
                this.$store.commit('SET_STORE', {
                    key: 'globalLoading',
                    value: false
                });
                if (err.response.status === 401) {
                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: '登录过期，请重新登录',
                    timer: 3000,
                  });
                  this.$router.push("/login")
                }
                else {
                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: err,
                    timer: 3000,
                  });
                }
              });
          this.loading = false;
      }
  }
};
</script>

<style lang="scss">
.words {
    .nya-btn{
        margin-bottom: 10px;
    }
    table {
        table-layout: auto;
        width: 100%;
        .translation{
            max-width: 500px;
        }
        .view-deep {
            cursor: pointer;
        }
    }
    .show-info {
        ul {
            margin: 0;
            padding: 0;
            li {
                list-style: none;
            }
        }
        ul.info {
            margin: 15px 0;
            li {
                line-height: 1.3;
                .title {
                    font-weight: bold;
                }
            }
        }
        .view-cdn-list {
            li {
                cursor: pointer;
            }
        }
    }
    .cdnjs_modal {
        padding: 15px;
        border-radius: 5px;
        background-color: var(--t2);
        max-width: 100%;
        font-size: 18px;
        .title {
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            padding-bottom: 15px;
            border-bottom: 1px solid #dad9d9;
            .start-speed {
                display: inline-block;
                font-size: 14px;
                padding: 2px 8px;
                border: 1px solid var(--border-color);
                margin-left: 5px;
                cursor: pointer;
            }
        }
        table {
            .cdnlink {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 250px;
            }
        }
    }
    // .fullversion_modal {
    // }
}
</style>
