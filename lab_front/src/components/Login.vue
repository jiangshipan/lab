<template>
  <div class="login-container">
    <div class="login">
      <el-input v-model="username" placeholder="请输入用户名"/>
      <el-input v-model="password" placeholder="请输入密码" show-password/>
      <el-button id="login_button" type="primary" @click="login()">立即登录</el-button>
      <router-link to="/reg">
        <el-link id="reg_link" :underline="false" type="primary">没有账号,去注册?</el-link>
      </router-link>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {base_url} from "../assets/js/base";

  export default {
    name: 'Login',
    data () {
      return {
        username: '',
        password: '',
        login_url: base_url + 'user/login'
      }
    },
    methods: {
      login() {
        if (this.username == '' || this.password == '') {
          this.errorMsg("缺少相关参数");
          return;
        }
        var url = this.login_url + "?username=" + this.username + "&password=" + this.password;
        axios.get(url)
        .then(response => {
          if (response.data.code != 0) {
            this.errorMsg(response.data.msg);
          } else {
            //跳转到主页面
            alert('登陆成功')
            this.$router.push({ path: '/' })
          }
        })
        .catch(error => {
          this.errorMsg(error)
        })
      },
      successMsg(msg) {
        this.$message({
          showClose: true,
          message: msg,
          type: 'success',
          duration: 2000
        });
      },
      errorMsg(msg) {
        this.$message({
          showClose: true,
          message: msg,
          type: 'error',
          duration: 2000
        });
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login {
    text-align: center;
    width: 300px;
  }
  #login_button {
    width: 300px;
    margin-top: 10px;
  }
  #reg_link {
    margin-top: 10px;
  }
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background: url("../assets/images/background.jpeg") no-repeat center center;
    background-size: cover;
  }
</style>
