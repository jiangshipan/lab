import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Register from '../components/Register'
import Index from '../components/Index'
import UserManager from '../components/UserManager'
import AddExperiment from '../components/AddExperiment'
import LabManager from '../components/LabManager'
import AddHelp from '../components/AddHelp'
import AddEmail from '../components/AddEmail'
import ExperimentManager from '../components/ExperimentManager'
import HelpManager from '../components/HelpManager'
import AddLab from '../components/AddLab'
Vue.use(Router)

export default new Router({
  routes: [{
      path: '/login',
      name: 'Login',
      component: Login
    },{
      path: '/reg',
      name: 'Register',
      component: Register
    },{
      path: '/experiment/add',
      name: 'AddExperiment',
      component: AddExperiment
    },
    {
      path: '/',
      name: 'Index',
      component: Index,
      children: [
        {
          path: '/UserManager',
          name: 'UserManager',
          component: UserManager
        }, {
          path: '/LabManager',
          name: 'LabManager',
          component: LabManager
        }, {
          path: '/ExperimentManager',
          name: 'ExperimentManager',
          component: ExperimentManager
        },{
          path: '/HelpManager',
          name: 'HelpManager',
          component: HelpManager
        }]
    }, {
      path: '/help/add',
      name: 'AddHelp',
      component: AddHelp
    }, {
      path: '/email/add',
      name: 'AddEmail',
      component: AddEmail
    },{
      path: '/lab/add',
      name: 'AddLab',
      component: AddLab
    }
  ]
})
