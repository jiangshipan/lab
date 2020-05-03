<template>
    <div class="user_manager">
        <el-table :data="user_list" style="width: 100%" border size="medium">
            <el-table-column prop="id" label="序号" align="center" type="index" :index="indexMethod"></el-table-column>
            <el-table-column prop="username" label="用户名" align="center"></el-table-column>
            <el-table-column prop="role" label="人员类型" align="center"></el-table-column>
            <el-table-column prop="contacts" label="联系方式" align="center"></el-table-column>
        </el-table>
    </div>
</template>

<script>
import axios from 'axios'
import {base_url} from "../assets/js/base";
axios.defaults.withCredentials =true;


export default {
    name: 'UserManager',
    data() {
        return {
           user_list: [],
           get_all_users: base_url + 'user/getAll',
        }
    },
    mounted() {
        this.get_all_user_infos();
    },
    methods: {
      get_all_user_infos() {
        axios.get(this.get_all_users)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.user_list = res.data;
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
      indexMethod(index) {
        return index + 1;
      }
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