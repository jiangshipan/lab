<template>
  <div class="main">
    <el-container>
      <el-header>
        <el-link class="el-link1" v-if="identity_type != '学生'" @click="redirect_input()">新增实验</el-link>
        <el-link class="el-link1" v-if="identity_type == '管理员'" @click="redirect_input3()">新增实验室</el-link>
        <el-link class="el-link1" @click="redirect_input1()">新增反馈</el-link>
        <el-link class="el-link1" v-if="identity_type != '学生'" @click="redirect_input2()">发送公告</el-link>
        <el-dropdown trigger="click" class="user-side">
          <span class="el-dropdown-link">
            你好, {{real_name}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="open_email()">站内信</el-dropdown-item>
              <el-dropdown-item @click.native="doOption('确认退出吗?')">退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>          
      </el-header>
      <el-container >
        <el-aside width="200px">
          <el-menu
            default-active="1"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-menu-item index="1" v-if="identity_type == '管理员'">
              <i class="el-icon-user"></i>
              <router-link tag="span" slot="title" to="/UserManager">用户管理</router-link>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-s-check"></i>
              <router-link v-if="identity_type != '学生'" tag="span" slot="title" to="/ExperimentManager">教学管理</router-link>
              <router-link v-if="identity_type == '学生'" tag="span" slot="title" to="/ExperimentManager">教学实验</router-link>
            </el-menu-item>
            <el-menu-item index="3" v-if="identity_type == '管理员'">
              <i class="el-icon-s-home"></i>
              <router-link tag="span" slot="title" to="/LabManager">实验室管理</router-link>
            </el-menu-item>
            <el-menu-item index="4" v-if="identity_type == '管理员'">
              <i class="el-icon-edit-outline"></i>
              <router-link tag="span" slot="title" to="/HelpManager">实验反馈</router-link>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
  import axios from 'axios'
  import {base_url} from "../assets/js/base";
  axios.defaults.withCredentials = true;
  export default {
    name: 'Index',
    data() {
      return {
        user_id: '',
        real_name: '',
        identity_type: '',
        email_infos: [{
          content: '1',
          create_name: '2',
          create_time: '3'
        },{
          content: '1',
          create_name: '2',
          create_time: '3'
        }],
        centerDialogVisible: false,
        get_user_url: base_url + 'user/get',
        get_email_url: base_url + 'email/get',

        logout_url: base_url + 'user/logout'
      }
    },
    mounted() {
      this.get_user_info();
      this.get_email();
    },
    methods: {
      get_user_info() {
        axios.get(this.get_user_url)
        .then(response => {
            var res = response.data;
            if (res.code == 0) {
              this.user_id = res.data.id;
              this.real_name = res.data.username;
              this.identity_type = res.data.role;
            } else {
              this.errorMsg("你好, 请登录")
              this.$router.push({ path: '/login' })
            }
        })
        .catch(error => {
          this.errorMsg('网络错误, 暂时不能访问')
        })
      },
      get_email() {
        axios.get(this.get_email_url)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
              this.errorMsg(res.msg)
            }
            this.email_infos = res.data
        })
        .catch(error => {
          this.errorMsg('网络错误, 暂时不能访问')
        })
      },
      logout() {
        axios.get(this.logout_url)
        .then(response => {
          var res = response.data;
          this.successMsg("注销成功");
          this.$router.push({ path: '/login' })
        })
        .catch(error => {
          this.errorMsg('网络错误, 暂时不能访问')
        })
      },
      redirect_input() {
        this.$router.push({ path: '/experiment/add'})
      },
      redirect_input1() {
        this.$router.push({ path: '/help/add'})
      },
      redirect_input2() {
        this.$router.push({ path: '/email/add',  query: {identity_type: this.identity_type}})
      },
      redirect_input3() {
        this.$router.push({ path: '/lab/add'})
      },
      doOption(msg) {
        this.$confirm(msg, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.logout();
        }).catch(() => {
          this.successMsg('已取消')     
        });
      },
      open_email() {
        var html = ''
        for (var i = 0; i < this.email_infos.length; i++) {
            var content = this.email_infos[i].content
            var create_name = this.email_infos[i].create_name
            var create_time = this.email_infos[i].create_time
            html = html.concat('<p>' + content + '&nbsp&nbsp' + create_name + '&nbsp&nbsp' + create_time +  '</p>')
        }
        this.$alert(html, '站内信', {
            dangerouslyUseHTMLString: true,
            center: false,
          });
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

<style scoped>
  .el-header {
    background-color: #B3C0D1;
    line-height: 60px;
  }
  .el-aside {
    text-align: center;
    background-color: #545c64
  }
  .el-main {
    padding: 0px;
  }
  .user-side {
    position:absolute;
    right: 2%
  }
  .main {
    display: flex;
    height: 100vh;
  }
  .el-menu {
    border-right: none;
  }
  .el-link1 {
    padding-left: 30px;
    padding-right: 30px;
  }
  .customer_div {
      width: 100%;
      height: 100%;
      background-color: beige
  }


</style>
