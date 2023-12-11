const store = new Vuex.Store({
    state: {
        token: null,
        uid: null,
        pid: null,
        ptitle: null,
        pbody: null,
        search_post_results: [],
        search_test_results: [],
        posts_list: [],
        tests_list: [],
        edu_records: [],
        edu_1: null,
        edu_2: null,
        edu_3: null,
        edu_id: null,
        user_details: null
    },
    mutations: {
        set_token(state,token){
            state.token = token
        },
        set_uid(state,uid){
            state.uid = uid
        },
        set_pid(state,pid){
            state.pid = pid
        },
        set_ptitle(state,ptitle){
            state.ptitle = ptitle
        },
        set_pbody(state,pbody){
            state.pbody = pbody
        },
        set_search_post_results(state,spr){
            state.search_post_results = spr
        },
        set_search_test_results(state,stres){
            state.search_test_results = stres
        },
        set_posts_list(state,plist){
            state.posts_list = plist
        },
        set_tests_list(state,tlist){
            state.tests_list = tlist
        },
        set_edu(state,edu){
            state.edu_records = edu
        },
        set_edu1(state,edu1){
            state.edu_1 = edu1
        },
        set_edu2(state,edu2){
            state.edu_2 = edu2
        },
        set_edu3(state,edu3){
            state.edu_3 = edu3
        },
        set_edu_id(state,edu_id){
            state.edu_id = edu_id
        },
        set_user_details(state,usede){
            state.user_details = usede
        }
    },
    getters: {
        get_token: function(state) {
            return (state.token);
        },
        get_uid: function(state) {
            return (state.uid);
        },
        get_pid: function(state) {
            return (state.pid);
        },
        get_ptitle: function(state) {
            return (state.ptitle);
        },
        get_pbody: function(state) {
            return (state.pbody);
        },
        get_search_post_results: function(state) {
            return (state.search_post_results);
        },
        get_search_test_results: function(state) {
            return (state.search_test_results);
        },
        get_posts_list: function(state) {
            return (state.posts_list);
        },
        get_tests_list: function(state) {
            return (state.tests_list);
        },
        get_edu: function(state) {
            return (state.edu_records)
        },
        get_edu1: function(state) {
            return (state.edu_1)
        },
        get_edu2: function(state) {
            return (state.edu_2)
        },
        get_edu3: function(state) {
            return (state.edu_3)
        },
        get_edu_id: function(state) {
            return (state.edu_id)
        },
        get_user_details: function(state){
            return (state.user_details)
        }
    }
});

const Login = Vue.component('login', {
    template: `
    <div>
        <h1>Login</h1>
            {{ login_message }}
        <label for="user_email"> Email </label>
        <input type="email" id="user_email" v-model= "user_email" />
        <label for="user_password"> Password </label>
        <input type="password" id="user_password" v-model="user_password" />
        <button v-on:click="check_creds">Login</button>
        <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
        <p>Forgot Password? <router-link to="/forgotpassword">Reset here</router-link></p>
    </div>
    `,
    data: function() {
        return {
            user_email: null,
            user_password: null,
            login_message: "Enter your details"
          } 
    },
    methods: {
        check_creds() {
            fetch( '/auth/login', {
              method: 'POST',
              headers: {
                'Content-Type' : 'application/json',
              },
              body: JSON.stringify({
                "email" : this.user_email,
                "password" : this.user_password,
              }),
            }
      
            )
            .then(response => response.json())
            .then(data => {
              if (data['status'] == "ok"){
                this.login_message = "Login successful"
                store.commit('set_token', data['jwt_token'])
                store.commit('set_uid', data['user_id'])
                fetch("/home/", {
                    method: 'GET',
                    headers: {
                        'Content-Type' : 'application/json',
                        'x-access-token' : this.$store.getters.get_token,  
                    },
                    body: null
                })
                .then(response => response.json())
                .then(data => {
                    this.$store.commit("set_posts_list",data['data'])
                })
                router.push({path: '/homepage'})
              }
              else {
                this.login_message = "Incorrect details. Please try again";
              }
            });
          }  
    }
})

const Register = Vue.component("register", {
    template: `
    <div>
        <h1>Sign Up</h1>
        {{ register_message }}
        <label for ="user_fname">First Name</label>
        <input type="text" id="user_fname" v-model="user_fname" />
        <label for ="user_lname">Last Name</label>
        <input type="text" id="user_lname" v-model="user_lname" />
        <label for ="user_email">Email</label>
        <input type="email" id="user_email" v-model="user_email" />
        <label for ="user_password">Password</label>
        <input type="password" id="user_password" v-model="user_password" />
        <button v-on:click="log_creds">Sign Up</button>
        <p>Already have an account? <router-link to="/login">Sign In</router-link></p>
    </div>
    `,
    data: function() {
        return {
            user_fname: null,
            user_lname: null,
            user_email: null,
            user_password: null,
            register_message: "Enter your details"
          }
    },
    methods: {
        log_creds() {
          fetch( '/auth/register', {
            method: 'POST',
            headers: {
              'Content-Type' : 'application/json',
            },
            body: JSON.stringify({
              "first_name" : this.user_fname,
              "last_name" : this.user_lname,
              "email" : this.user_email,
              "password" : this.user_password,
            }),
          }
    
          )
          .then(response => response.json())
          .then(data => {
            if (data['status'] == 'ok'){
              this.register_message = "Registration successful"
              router.push({path: '/'})
            }
            else {
              this.register_message = "Incorrect details. Please try again";
            }
          });
        }
      }
})

const Homepage = Vue.component('homepage', {
    props: ["item","index"],
    template: `
    <div>
        <h3> Home </h3>
        <label for="search_query"> Search Query </label>
        <input type="text" id="search_query" v-model="search_query" />
        <button v-on:click="search_posts">Search</button>
        <button v-on:click="create_post">Create Post </button>
        <button v-on:click="view_profile">Profile </button>
        <p v-for="(item,index) in plist":key="index">
            {{ item["post_title"] }}
            <br>
            <button v-on:click="view_post(item['post_id'],item['post_title'],item['post_caption'])"> View Post </button>
        </p>
    </div>
    `,
    data: function() {
        return {
            search_query : null,
        }
    },
    methods: {
        search_posts() {
            fetch( `/search/posts/${this.search_query}`, {
              method: 'GET',
              headers: {
                'x-access-token' : this.$store.getters.get_token,
              },
              body: null,
            }
      
            )
            .then(response => response.json())
            .then(data => {
                this.$store.commit('set_search_post_results',data['data'])
                router.push({path: '/searchresults'})
            });
          },
          create_post() {
            router.push({path: '/createpost'})
          },
          browse_tests() {
            router.push({path: '/browsetests'})
          },
          view_post(po_id,po_title,po_body) {
            this.$store.commit('set_pid',po_id)
            this.$store.commit('set_ptitle',po_title)
            this.$store.commit('set_pbody',po_body)
            router.push({path: '/viewpost'})
          },
          view_profile() {
            fetch(`/profile/${this.$store.getters.get_uid}`, {
                method: 'GET',
                headers: {
                    'x-access-token' : this.$store.state.token
                },
                body: null
            })
            .then(response => response.json())
            .then(data => {
                this.$store.commit("set_edu",data['data'])
                this.$store.commit("set_user_details", data['user'])
                router.push({path: '/viewprofile'})
            })
          }
    },
    computed: {
        plist(){
            return this.$store.getters.get_posts_list;
        }
    }
})

const Searchresults = Vue.component('searchresults', {
    props: ["item","index"],
    template: `
    <div>
        <h3> Results </h3>
        <label for="search_query"> Search Query </label>
        <input type="text" id="search_query" v-model="search_query" />
        <button v-on:click="search_posts">Search</button>
        <p v-for="(item,index) in plist":key="index">
            {{ item["post_title"] }}
            <br>
            <button v-on:click="view_post(item['post_id'],item['post_title'],item['post_caption'])"> View Post </button>
        </p>
        <br>
        <p> <router-link to="/homepage">Return to Home</router-link></p>
    </div>    
    `,
    data: function() {
        return {
            search_query : null,
        }
    },
    methods: {
        search_posts() {
            fetch( `/search/posts/${this.search_query}`, {
              method: 'GET',
              headers: {
                'x-access-token' : this.$store.getters.get_token,
              },
              body: null,
            }
      
            )
            .then(response => response.json())
            .then(data => {
                this.$store.commit('set_search_post_results',data['data'])
                router.push({path: '/searchresults'})
            });
          },
          view_post(po_id,po_title,po_body) {
            this.$store.commit('set_pid',po_id)
            this.$store.commit('set_ptitle',po_title)
            this.$store.commit('set_pbody',po_body)
            router.push({path: '/viewpost'})
          }
    },
    computed: {
        plist(){
            return this.$store.getters.get_search_post_results;
        }
    }
})

const Createpost = Vue.component('createpost', {
    template: `
    <div>
        <h3> Create New Post </h3>
            {{ post_message }}
        <label for="post_title"> Post Title </label>
        <input type="text" id="post_title" v-model="post_title" />
        <label for="post_body"> Post Body </label>
        <textarea id="post_body" v-model="post_body" />
        </textarea>
        <button v-on:click="create_post">Submit</button> 
        <p> <router-link to="/homepage">Return to Home</router-link></p>  
    </div>
    `,
    data: function() {
        return {
            post_title: null,
            post_body: null,
            post_message: "Enter your details"
          } 
    },
    methods: {
        create_post() {
          fetch( '/post/', {
            method: 'POST',
            headers: {
              'Content-Type' : 'application/json',
              'x-access-token' : this.$store.getters.get_token,
    
            },
            body: JSON.stringify({
              "post_title" : this.post_title,
              "post_caption" : this.post_body,
            }),
          })
          .then(response => response.json())
          .then(data => {
            if (data['status'] == 'ok'){
              this.post_message = "Post successful"
              this.$store.commit('set_pid', data['post_id'])
              this.$store.commit('set_ptitle', this.post_title)
              this.$store.commit('set_pbody', this.post_body)
              router.push({path: '/viewpost'})
              }
            else {
              this.post_message = "Incorrect details. Please try again";
            }
          });
        }
    }
})

const Viewpost = Vue.component("viewpost", {
    template: `
    <div>
      <h1>{{ post_title }}</h1>
      <p>{{ post_body }}</p>
      <br>
        <button v-on:click="edit_post()"> Edit </button>
        <button v-on:click="delete_post()"> Delete </button>
      <br>
      <p> <router-link to="/homepage">Return to Home</router-link></p>
        {{ view_message }}
    </div>
    `,
    data: function() {
        return {
            post_title : this.$store.getters.get_ptitle,
            post_body : this.$store.getters.get_pbody,
            view_message: null
          }
    },
    methods: {
      edit_post() {
        router.push({path: "/editpost"})
      },
      delete_post() {
        fetch(`/post/${this.$store.getters.get_pid}`, {
          method: 'DELETE',
          headers: {
            'Content-Type' : 'application/json',
            'x-access-token' : this.$store.getters.get_token,
          },
          body: null,
        })
        .then(response => response.json())
        .then(data => {
                if (data['status'] == 'ok'){
                  this.$store.commit("set_posts_list",data['data'])
                  router.push({path:"/homepage"})
                  }
                else{
                  this.view_message = "unauthorized"
                  }
              })
      }
    }
})

const Editpost = Vue.component("editpost", {
    template: `
    <div>
        <h3> Edit Post </h3>
            {{ post_message }}
        <label for="post_title"> Post Title </label>
        <input type="text" id="post_title" v-model="post_title" />
        <label for="post_body"> Post Body </label>
        <textarea id="post_body" v-model="post_body" />
        </textarea>
        <button v-on:click="edit_post">Edit</button> 
        <p> <router-link to="/homepage">Return to Home</router-link></p>  
    </div>
    `,
    data: function() {
        return {
            post_title: this.$store.getters.get_ptitle,
            post_body: this.$store.getters.get_pbody,
            post_message: "Enter your details"
          } 
    },
    methods: {
        edit_post() {
          fetch( `/post/${this.$store.getters.get_pid}`, {
            method: 'PUT',
            headers: {
              'Content-Type' : 'application/json',
              'x-access-token' : this.$store.getters.get_token,
    
            },
            body: JSON.stringify({
              "post_title" : this.post_title,
              "post_caption" : this.post_body,
            }),
          }
    
          )
          .then(response => response.json())
          .then(data => {
            if (data['status'] == 'ok'){
              this.post_message = "Edit successful"
              store.commit('set_pid', data['post_id'])
              store.commit('set_ptitle',this.post_title)
              store.commit('set_pbody',this.post_body)
              router.push({path: '/viewpost'})
            }
            else {
              this.post_message = "Incorrect details. Please try again";
            }
          });
        }
    }

})

const Viewprofile = Vue.component("viewprofile", {
    props: ["item","index"],
    template: `
    <div>
        <h3> Profile </h3>
        <br>
        {{ user["first_name"] }}
        {{ user["last_name"] }}
        <br>

            <p v-for="(item,index) in elist":key="index">
                {{ item["college_name"] }}
                <br>
                {{ item["joining_year"] }} - {{ item["graduation_year"] }}
                <br>
                <button v-on:click="edit_record(item['college_name'],item['joining_year'],item['graduation_year'],item['education_id'])"> Edit Record </button>
                <button v-on:click="delete_record(item['education_id'])"> Delete Record </button>
            </p>
            <h3> Add Record </h3>
            <label for="college_name"> College Name </label>
            <input type="text" id="college_name" v-model="college_name" />
            <label for="joining_year"> Joining Year </label>
            <input type="text" id="joining_year" v-model="joining_year" />
            <label for="graduation_year"> Graduation Year </label>
            <input type="text" id="graduation_year" v-model="graduation_year" />
            <button v-on:click="add_record">Submit</button>
            <p> <router-link to="/homepage">Return to Home</router-link></p>
    </div>
    `,
    data: function() {
        return {
            college_name : null,
            joining_year : null,
            graduation_year : null,
            user : this.$store.getters.get_user_details
        }
    },
        methods: {
            add_record() {
                fetch( 'achievement/education', {
                  method: 'POST',
                  headers: {
                    'Content-Type' : 'application/json',
                    'x-access-token' : this.$store.getters.get_token,
                  },
                  body: JSON.stringify ({
                    "college_name" : this.college_name,
                    "joining_year" : this.joining_year,
                    "graduation_year" : this.graduation_year
                  }),
                }
                )
                .then(
                    router.push({path:"/homepage"})
                )
              },
              delete_record(ed_id_d) {
                fetch( `achievement/education/${ed_id_d}`, {
                    method: 'DELETE',
                    headers: {
                      'Content-Type' : 'application/json',
                      'x-access-token' : this.$store.getters.get_token,
                    },
                    body: null,
                  }
                  )
                  .then(response => response.json())
                  .then(data => {
                          this.$store.commit("set_edu",data['data'])
                          this.$forceUpdate()
                      })
              },
              edit_record(ed_1,ed_2,ed_3, ed_id) {
                this.$store.commit('set_edu1',ed_1)
                this.$store.commit('set_edu2',ed_2)
                this.$store.commit('set_edu3',ed_3)
                this.$store.commit('set_edu_id',ed_id)
                router.push({path: '/editedu'})
              }
        },
        computed: {
            elist(){
                return this.$store.getters.get_edu;
            }
        }
})

const Editedu = Vue.component("editedu", {
    template: `
    <div>
    <h3> Edit Record </h3>
            <label for="college_name"> College Name </label>
            <input type="text" id="college_name" v-model="college_name" />
            <label for="joining_year"> Joining Year </label>
            <input type="text" id="joining_year" v-model="joining_year" />
            <label for="graduation_year"> Graduation Year </label>
            <input type="text" id="graduation_year" v-model="graduation_year" />
            <button v-on:click="edit_record">Submit</button>
            <p> <router-link to="/viewprofile">Return to Profile</router-link></p>
    </div>
    `,
    data: function() {
        return {
            college_name : this.$store.getters.get_edu1,
            joining_year : this.$store.getters.get_edu2,
            graduation_year : this.$store.getters.get_edu3,
            edu_id : this.$store.getters.get_edu_id
        }
    },
   methods: {
    edit_record: function() {
        fetch(`/achievement/education/${this.edu_id}`, {
            method: 'PUT',
            headers: {
              'Content-Type' : 'application/json',
              'x-access-token' : this.$store.getters.get_token,
    
            },
            body: JSON.stringify({
              "college_name" : this.college_name,
              "joining_year" : this.joining_year,
              "graduation_year" : this.graduation_year
            }),
          })
          .then(
            fetch(`/profile/${this.$store.getters.get_uid}`, {
                method: 'GET',
                headers: {
                    'Content-Type' : 'application/json',
                    'x-access-token' : this.$store.state.token
                },
                body: null
            })
            .then(response => response.json())
            .then(
                router.push({path: '/homepage'})
            )
          )
    }
   }  
})

const routes = [{
    path: "/",
    component: Login
},
{
    path: "/register",
    component: Register
},
{
    path: "/homepage",
    component: Homepage
},
{
    path: "/searchresults",
    component: Searchresults
},
{
    path: "/createpost",
    component: Createpost
},
{
    path: "/viewpost",
    component: Viewpost
},
{
    path: "/editpost",
    component: Editpost
},
{
    path: "/viewprofile",
    component: Viewprofile
},
{
    path: "/editedu",
    component: Editedu
}
];

const router = new VueRouter({
    routes
})

var app = new Vue({
    el: '#app',
    delimiters: ['${','}'],
    router:router,
    store:store
})