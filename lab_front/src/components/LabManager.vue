<template>
    <div class="lab_manager">
        <el-table :data="lab_list" style="width: 100%" border size="medium">
            <el-table-column prop="id" label="序号" align="center"></el-table-column>
            <el-table-column prop="name" label="实验室名称" width="300" align="center"></el-table-column>
            <el-table-column prop="devices" label="资产" width="480" align="center"></el-table-column>
            <el-table-column prop="notice" label="公告" align="center"></el-table-column>
            <el-table-column label="操作" align="center">
            <template slot-scope="scope">
                <el-button type="primary" @click="doOption('请输入新的资产(请注意输入格式 key1:value1, key2:value2)', scope.row.id)">修改资产</el-button>
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
    name: 'LabManager',
    data() {
        return {
           lab_list: [],
           get_all_labs: base_url + 'laboratory/getAll',
           update_device: base_url + 'laboratory/update'
        }
    },
    mounted() {
        this.get_all_lab_infos();
    },
    methods: {
      get_all_lab_infos() {
        axios.get(this.get_all_labs)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.lab_list = res.data;
        })
        .catch(error => {
            this.errorMsg(error)
        }) 
      },
      update_devices(id, devices) {
        axios.get(this.update_device + "?lab_id=" + id + "&devices=" + devices)
        .then(response => {
            var res = response.data;
            if (res.code != 0) {
                this.errorMsg(response.data.msg);
                return;
            }
            this.successMsg("修改成功")
            this.get_all_lab_infos()
        })
        .catch(error => {
            this.errorMsg(error)
        }) 
      },
      doOption(msg, id) {
        this.$confirm(msg, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'info',
          showInput: true
        }).then(({value}) => {
          this.update_devices(id, value)
        }).catch(() => {
          this.successMsg('已取消')     
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