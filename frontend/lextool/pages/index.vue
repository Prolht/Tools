<template>
    <div class="home">
        <Welcome />
        <Favorites v-show="!searchText" />

        <nya-container
            v-if="$store.state.setting.hideCategory"
            v-show="!searchText"
            icon="shopping-bag-outline"
            title="工具"
        >
            <template v-for="(tool, index2) in toolsList">
                <nuxt-link
                    v-if="showBtn(tool)"
                    :key="index2"
                    :title="tool.name"
                    :to="tool.path"
                    class="nya-btn"
                    :class="[tool.hot, {'badge': tool.hot}]"
                >
                    {{ tool.name }}
                </nuxt-link>
            </template>
        </nya-container>

        <template v-else v-show="!searchText">
            <nya-container
                v-for="(item, index) in $store.state.tools"
                v-show="!searchText && showSection(item)"
                :key="index"
                :icon="item.icon"
                :title="item.title"
            >
                <template v-for="(tool, index2) in item.list">
                    <nuxt-link
                        v-if="showBtn(tool) && tool.path[0] === '/'"
                        :key="index2"
                        :target="$store.state.setting.inNewTab ? '_blank' : '_self'"
                        :title="tool.name"
                        :to="tool.path"
                        class="nya-btn"
                        :class="[tool.hot, {'badge': tool.hot}]"
                    >
                        {{ tool.name }}
                    </nuxt-link>
                    <a
                        v-else-if="showBtn(tool) && tool.path[0] !== '/'"
                        :key="index2"
                        :target="$store.state.setting.inNewTab ? '_blank' : '_self'"
                        :title="tool.name"
                        :href="tool.path"
                        class="nya-btn"
                        :class="[tool.hot, {'badge': tool.hot}]"
                    >
                        {{ tool.name }}
                    </a>
                </template>
            </nya-container>
        </template>

        <nya-container v-if="!$store.state.setting.hideNotice" v-show="!searchText" title="公告" icon="volume-down-outline">
            <ul class="nya-list">
                <li>前端致敬 <a href="https://tools.miku.ac/" target="_blank" rel="noopener noreferrer">MikuTools</a></li>
                <li>
                    <div class="badge-info">
                        <span class="badge hot">热门</span> <span class="badge debug">debug中</span> <span class="badge new">新功能</span> <span class="badge recommend">推荐</span>
                    </div>
                </li>
                <li><b>欢迎将本站收藏到收藏夹，以便以后使用</b></li>
<!--                <li>-->
<!--                    本站域名：<a-->
<!--                        :href="$store.state.env.url"-->
<!--                        target="_blank"-->
<!--                        rel="noopener noreferrer"-->
<!--                    >{{ $store.state.env.domain }}</a>-->
<!--                </li>-->
                <li v-if="$store.state.isMobile.any">
                    如果遇到无法使用或者样式问题，请更换浏览器后重试，推荐使用 Chrome 浏览器，对 iOS 设备兼容性可能不太好
                </li>
                <li v-on:click="wantpay" style="cursor: pointer">
                    觉得不错？点我
                </li>
            </ul>
        </nya-container>

        <nya-container v-if="!$store.state.setting.hidePay && !hidepay" v-show="!searchText" title="打赏" icon="credit-card-outline">
            <ul class="pay">
                <li>
                    <img src="../assets/wechat.png" alt="weixin">
                    <div class="name">
                        微信
                    </div>
                </li>
                <li>
                    <img src="../assets/alipay.png" alt="alipay">
                    <div class="name">
                        支付宝
                    </div>
                </li>
            </ul>
        </nya-container>
    </div>
</template>

<script>
import Favorites from '~/components/Favorites';
// import Search from '~/components/Search';
import isMobile from 'ismobilejs';
import Welcome from '~/components/Welcome';
export default {
    name: 'Home',
    components: {
        Favorites,
        // Search,
        Welcome
    },
    head() {
        return {
            title: this.name
        };
    },
    data() {
        return {
            title: `${process.env.title} - ${process.env.description}`,
            searchText: '',
            isMobile,
            hidepay:true,
            loading: false
        };
    },
    computed: {
        toolsList() {
            let arr = [];
            this.$store.state.tools.forEach(tool => {
                arr = arr.concat(tool.list);
            });
            return arr;
        }
    },
    mounted(){
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'success',
            title: '欢迎光临本站！',
            timer: 1500,
            showConfirmButton:false,
        });
    },
    methods: {
        wantpay(){
            this.hidepay = !this.hidepay;
        },
        enterFirst(e) {
            if (this.$store.state.setting.inNewTab) {
                window.open(e.path);
            } else {
                this.$router.push(e.path);
            }
        },
        showSection(item) {
            return !(
                item.list.filter(i => {
                    return (
                        this.$store.state.setting.hide.indexOf(i.path) !== -1
                    );
                }).length === item.list.length
            );
        },
        showBtn(tool) {
            return this.$store.state.setting.hide.indexOf(tool.path) === -1;
        }
    }
};
</script>

<style lang="scss">
.home {
    span.mb {
        display: block;
        margin-bottom: 15px;
    }
    table {
        width: 100%;
        table-layout: auto;
    }
    ._ad {
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .nya-btn {
        position: relative;
        margin: 7px;
        width: calc(20% - 14px);
        text-align: center;
        box-sizing: border-box;
        overflow: hidden;
        text-align: center;
        text-overflow: ellipsis;
        white-space: nowrap;
        transition: all 0.3s ease;
        /*background-color: transparent;*/
        font-size: 18px;
        border-radius: 10px;
        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px 0px rgba(10, 14, 29, 0.04),
                0px 8px 64px 0px rgba(10, 14, 29, 0.08);
            border-color: #024466;
            color: #ffffff;
            /*background-color: var(--theme);*/
            /*border-color: var(--theme);*/
            /*color: var(--theme);*/
            background-color: #024466;
        }
        @media (max-width: 1050px) {
            width: calc(25% - 14px);
        }
        @media (max-width: 900px) {
            width: calc(100% / 3 - 14px);
        }
        @media (max-width: 700px) {
            box-shadow: none;
            margin: 5px;
            width: calc(50% - 10px);
        }
    }
    .pay {
        width: 100%;
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: space-around;
        li {
            margin: 0;
            list-style: none;
            padding: 10px;
            .name {
                text-align: center;
                font-size: 25px;
                font-weight: bold;
                margin-top: 5px;
            }
            img {
                width: 200px;
                max-width: 100%;
            }
        }
    }
    .badge {
        &::after {
            content: '';
            position: absolute;
            top: 5px;
            right: 5px;
            color: #fff;
            font-weight: lighter;
            text-shadow: 1px 1px 1px rgba($color: #000000, $alpha: 0.2);
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        &.new::after {
            background-color: var(--theme-success);
        }
        &.hot::after {
            background-color: var(--theme-danger);
        }
        &.debug::after {
            background-color: #f79817;
        }
        &.recommend::after {
            background-color: var(--theme);
        }
    }
    .badge-info {
        display: inline-flex;
        align-items: center;
        .badge {
            display: inline-flex;
            margin-right: 10px;
            align-items: center;
            &::after {
                position: relative;
                left: auto;
                margin-left: 10px;
                top: auto;
                display: inline-block;
            }
        }
    }
}
</style>
