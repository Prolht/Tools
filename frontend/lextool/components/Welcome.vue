<template>
    <nya-container v-if="$store.state.welcome" class="welcome">
        <h2 style="font-family: 'Times New Roman'">Welcome to Muggle's World</h2>
        <p>
          <span style="font-family: 'Times New Roman'">
            Spruce wood with a unicorn hair core, 11" and solid flexibility
            [云杉木，独角兽内芯，11英寸，柔韧性偏硬]
          </span>
          <br>
          这是我自己开发或收集的小工具合集，若有新的工具欢迎提建议。
          <a href="/comment_board">
            在这儿留言
          </a>
        </p>
        <div class="close" title="关闭" @click="close">
            <i class="eva eva-close-outline"></i>
        </div>
    </nya-container>
</template>

<script>
export default {
    name: 'Welcome',
    methods: {
        close() {
            this.$store.commit('SET_STORE', {
                key: 'welcome',
                value: false
            });
        }
    }
};
</script>

<style lang="scss">
.nya-container.welcome {
    margin-bottom: 32px;
    margin-top: 18px;
    .close {
        cursor: pointer;
        $width: 30px;
        position: absolute;
        right: -12px;
        top: -12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        width: $width;
        height: $width;
        border-radius: 50%;
        color: #fff;
        background-color: var(--theme);
        box-shadow: 0 8px 10px rgba(36, 159, 253, 0.30196);
    }
}
</style>
