<template>
    <div class="help_manager">
        <el-table :data="help_list" style="width: 100%" border size="medium">
            <el-table-column prop="id" label="序号" align="center" width="100"></el-table-column>
            <el-table-column prop="lab_name" label="实验室名称" width="300" align="center"></el-table-column>
            <el-table-column prop="question" label="问题" width="480" align="center"></el-table-column>
            <el-table-column prop="status" label="状态" align="center"></el-table-column>
            <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                    <el-button v-if="identity_type == '管理员' && scope.row.status != '已处理'" type="primary" @click="update_status(scope.row.id, 0)">已处理</el-button>
                    <el-button v-if="identity_type == '管理员' && scope.row.status != '未处理'" type="danger" @click="update_status(scope.row.id, 1)">未处理</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import axios from 'axios'
import {base_url} from "../assets/js/base";
axios.defaults.withCredentials =true;


export default {
    name: 'HelpManager',
    data() {
        return {
           help_list: [],
           get_all_helps: base_url + 'laboratory/get_all_helps',
           get_user_url: base_url + 'user/get',
           update_help_status: base_url + 'laboratory/do_help'
        }
    },
    mounted() {
        this.get_all_help_infos();
        this.get_user_info();
    },
    methods: {
     get_user_info() {
        axios.get(this.get_user_url)
        .then(response => {
            var res = response.data;
            if (res.code == 0) {
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
      get_all_help_infos() {
        axios.get(this.get_all_helps)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.help_list = res.data;
        })
        .catch(error => {
            this.errorMsg(error)
        }) 
      },
      update_status(id, status) {
        axios.get(this.update_help_status + "?hid=" + id + "&status=" + status)
            .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.successMsg("操作成功")
            this.get_all_help_infos()
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
      }, 
    }
}
</script>

<style scoped>
  .input-container {
    display: flex;
    justify-content: space-between;
    width: 1000px;
    margin: 50px 0 10px 0;
  }
  .block {
    margin: auto;
    width: 40%;
    margin-top: 10px;
  }

</style>