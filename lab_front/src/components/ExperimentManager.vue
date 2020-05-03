<template>
    <div class="experiment_list">
        <el-table :data="experiment_list" style="width: 100%" border size="medium">
            <el-table-column prop="id" label="序号" align="center" width="50"></el-table-column>
            <el-table-column prop="name" label="实验名称" align="center"></el-table-column>
            <el-table-column prop="lab_name" label="实验室" align="center"></el-table-column>
            <el-table-column prop="remark" label="实验内容" align="center"></el-table-column>
            <el-table-column prop="start_time" label="开始时间" align="center"></el-table-column>
            <el-table-column prop="end_time" label="结束时间" align="center"></el-table-column>
            <el-table-column prop="teacher_name" label="负责教师" align="center"></el-table-column>
            <el-table-column v-if="identity_type != '学生'" prop="all_selects" label="已选同学" align="center"></el-table-column>
            <el-table-column v-if="identity_type != '学生'" prop="status" label="状态" align="center"></el-table-column>
            <el-table-column v-if="identity_type != '教师'" label="操作" align="center">
                <template slot-scope="scope">
                    <el-button v-if="identity_type == '管理员' && scope.row.status != '审批通过'" type="primary" @click="update_status(scope.row.id, 0)">通过</el-button>
                    <el-button v-if="identity_type == '管理员' && scope.row.status != '审批未通过'" type="danger" @click="update_status(scope.row.id, 2)">拒绝</el-button>
                    <el-button v-if="identity_type == '学生' && !judge(username, scope.row.all_selects)" type="primary" @click="join_experiment(scope.row.id)">选择</el-button>
                    <el-button v-if="identity_type == '学生' && judge(username, scope.row.all_selects)"   disabled type="success">已选择</el-button>
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
    name: 'ExperimentManager',
    data() {
        return {
           experiment_list: [],
           identity_type: '',
           user_name: '',
           select_list: [],
           get_all_experiments: base_url + 'experiment/get',
           update_experiment_status: base_url + 'experiment/update',
           get_user_url: base_url + 'user/get',
           join_experiment_url: base_url + 'experiment/join'
        }
    },
    mounted() {
        this.get_all_experiment_infos();
        this.get_user_info();

    },
    methods: {
    get_user_info() {
        axios.get(this.get_user_url)
        .then(response => {
            var res = response.data;
            if (res.code == 0) {
              this.identity_type = res.data.role;
              this.username = res.data.username
            } else {
              this.errorMsg("你好, 请登录")
              this.$router.push({ path: '/login' })
            }
        })
        .catch(error => {
          this.errorMsg('网络错误, 暂时不能访问')
        })
      },
    get_all_experiment_infos() {
        axios.get(this.get_all_experiments)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.experiment_list = res.data;
        })
        .catch(error => {
            this.errorMsg(error)
        }) 
      },
    judge(username, list) {
      for (var i = 0; i < list.length; i++) {
        if (username == list[i]) {
          return true
        }
      }
      return false
    },
    update_status(id, status) {
        axios.get(this.update_experiment_status + "?eid=" + id + "&status=" + status)
            .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.successMsg("操作成功")
            this.get_all_experiment_infos()
        })
        .catch(error => {
            this.errorMsg(error)
        }) 
    },
    join_experiment(id) {
        axios.get(this.join_experiment_url + "?eid=" + id)
            .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.successMsg("选择成功")
            this.get_all_experiment_infos()
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