<template>
    <div class="links">
        <nya-container :title="title">
            <div v-for="(item, index) in links" :key="index">
                <div class="nya-subtitle">
                    {{ item.title }}
                </div>
                <ul class="nya-list">
                    <li v-for="(list, index2) in item.list" :key="index2">
                        <span v-if="list.name">{{ list.name }}：</span>
                        <a
                            v-if="list.link"
                            :title="list.description"
                            :href="list.link"
                            target="_blank"
                            rel="noopener noreferrer"
                        >{{ list.link }}</a>
                        <a v-else href="javascript:;">暂无网站</a>
                    </li>
                </ul>
            </div>
            <div>
                <div class="nya-subtitle">
                    感谢以下项目(未全部列出)
                </div>
                <ul class="nya-list">
                    <li v-for="(item, index) in project" :key="index">
                        <a :href="item" target="_blank" rel="noopener noreferrer">{{ item }}</a>
                    </li>
                </ul>
            </div>
        </nya-container>
    </div>
</template>

<script>
export default {
    name: 'Links',
    head() {
        return {
            title: this.title
        };
    },
    data() {
        return {
            title: '友情链接',
            links: [
                {
                    title: '主要维护人员',
                    list: [
                        {
                            name: 'Lex',
                            description: '简约不简单',
                            link: 'https://www.lex666.online/'
                        },
                        // {
                        //     name: 'Lex',
                        //     description: '维护人员',
                        //     link: 'https://www.lex666.online/'
                        // },
                        // {
                        //     name: 'Lex',
                        //     description: '图标设计',
                        //     link: 'https://www.lex666.online/'
                        // },
                    ]
                },
                {
                    title: '其他',
                    list: [
                        {
                            name: 'GitHub地址',
                            description: '有钱的捧个钱场，有人的捧个人场',
                            link: 'https://github.com/Prolht/Tools'
                        },
                    ]
                }
            ],
            project: [
                'https://github.com/hinesboy/mavonEditor/blob/master/README.md', //Markdown
                'https://akveo.github.io/eva-icons/', //icon
                'https://github.com/nuxt',
                'https://github.com/iamkun/dayjs',
                'https://github.com/expressjs/express',
                'https://github.com/ytdl-org/youtube-dl',
                'https://github.com/Binaryify/NeteaseCloudMusicApi',
                'https://github.com/cnwhy/nzh',
                'https://github.com/tsayen/dom-to-image',
                'https://github.com/akveo/eva-icons',
                'https://github.com/jnordberg/gif.js/',
                'https://github.com/cozmo/jsQR',
                'https://github.com/hinesboy/mavonEditor',
                'https://github.com/vinta/pangu.js',
                'https://github.com/alexeyten/qr-image',
                'https://github.com/mumuy/relationship',
                'https://github.com/nhnent/tui.image-editor',
                'https://github.com/mirari/v-viewer',
                'https://github.com/xiaokaike/vue-color',
                'https://github.com/Inndy/vue-clipboard2',
                'https://github.com/MoePlayer/vue-dplayer',
                'https://github.com/euvl/vue-js-modal',
                'https://github.com/surmon-china/vue-quill-editor',
                'https://github.com/NightCatSama/vue-slider-component',
                'https://github.com/highlightjs/highlight.js',
                'https://github.com/hotoo/pinyin',
                'https://github.com/shadowcz007/DYText',
                'https://github.com/egoist/video2gif',
                'https://github.com/lokesh/color-thief',
                'https://github.com/bgrins/TinyColor',
                'https://github.com/bunkat/later',
                'https://github.com/faisalman/ua-parser-js',
                'https://github.com/mengxiong10/vue2-datepicker',
                'https://github.com/gblazex/smoothscroll-for-websites',
                'https://github.com/kaimallea/isMobile',
                'https://github.com/axios/axios',
                'https://github.com/daniellmb/console.style',
                'https://github.com/Ice-Hazymoon/telegram_sticker_downloader',
                'https://github.com/Ice-Hazymoon/idcard_generator',
                'https://github.com/brix/crypto-js',
                'https://github.com/chanind/hanzi-writer',
                'https://github.com/niklasvh/html2canvas',
                'https://github.com/beautify-web/js-beautify',
                'https://github.com/josdejong/jsoneditor',
                'https://github.com/lodash/lodash',
                'https://github.com/typicode/lowdb',
                'https://github.com/markedjs/marked',
                'https://github.com/necolas/normalize.css/',
                'https://www.npmjs.com/package/tinycolor2',
                'https://github.com/hilongjw/vue-lazyload',
                'https://github.com/robinvdvleuten/vuex-persistedstate',
                'https://github.com/m13253/JPEGreen'
            ]
        };
    }
};
</script>
