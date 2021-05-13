let requestData = class {
  constructor(direction) {
    this.url = "/";
    this.direction = direction;
  }
  /////request to programz
  postData(url, data) {
    // Default options are marked with *

    return new Promise(function (resolve, reject) {
      fetch(url, {
        body: JSON.stringify(data), // must match 'Content-Type' header
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
          "content-type": "application/json",
        },
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // *client, no-referrer
      }).then((response) => {
        resolve(response.json());
      }); // parses response to JSON
    });
  }

  getData(data) {
    // Default options are marked with *
    let that = this;
    let url = "/status";
    return new Promise(function (resolve, reject) {
      fetch(url, {
        body: JSON.stringify(data), // must match 'Content-Type' header
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
          "content-type": "application/json",
        },
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // *client, no-referrer
      }).then((response) => {
        resolve(response.json());
      }); // parses response to JSON
    });
  }

  requestToPy(param) {
    let url = this.url + this.direction;
    let that = this;
    return new Promise(function (resolve, reject) {
      console.log(url);
      that.postData(url, param).then((res) => {
        resolve(res);
      });
    });
  }

  checkclass(classcode) {
    let param = {
      course_code: classcode,
    };
    let that = this;

    return new Promise(function (resolve, reject) {
      let url = this.url + this.direction;
      that.postData(url, param).then((res) => {
        resolve(res);
      });
    });
  }
};

function htmlreturn(alldata, originalcode) {
  let datacontain = [];
  return new Promise(function (resolve, reject) {
    alldata.forEach((data) => {
      let name = document.createElement("div");
      let code = document.createElement("div");
      let classes = document.createElement("div");
      let time = document.createElement("div");
      let room = document.createElement("div");
      let vacancy = document.createElement("div");
      let swapcourse = document.createElement("div");
      name.innerHTML = data.course_title;
      name.setAttribute("class", "item");
      code.innerHTML = data.course_code;
      code.setAttribute("class", "item");
      classes.innerHTML = data.class;
      classes.setAttribute("class", "item");
      time.innerHTML = data.time;
      time.setAttribute("class", "item");
      room.innerHTML = data.room;
      room.setAttribute("class", "item");
      vacancy.innerHTML = data.vacancy;
      vacancy.setAttribute("class", "item");
      swapcourse.setAttribute("class", "item");
      if (data.vacancy > 0) {
        name.setAttribute("style", "background-color:#99FF4D");
        code.setAttribute("style", "background-color:#99FF4D");
        classes.setAttribute("style", "background-color:#99FF4D");
        time.setAttribute("style", "background-color:#99FF4D");
        room.setAttribute("style", "background-color:#99FF4D");
        vacancy.setAttribute("style", "background-color:#99FF4D");
        swapcourse.setAttribute("style", "background-color:#99FF4D");
        // swapcourse.innerHTML = "swap to this class";
        // swapcourse.setAttribute('style', "cursor:pointer");
        // swapcourse.addEventListener('click', e => {
        //     // addDrop(data.course_code,data.course_code,data.class).then(res=>{
        //     //     alert(res.message)
        //     // })

        // })
      }

      swapcourse.innerHTML = "swap to this class";
      swapcourse.setAttribute("style", "cursor:pointer");
      swapcourse.addEventListener("click", (e) => {
        let param = {
          origin_code: originalcode,
          new_code: data.course_code,
          new_class: data.class,
          boost: false,
        };
        console.log(JSON.stringify(param), "add-drop param");
        new requestData("add-drop").requestToPy(param).then((res) => {
          alert(res.message);
        });
      });
      datacontain.push({
        name: name,
        code: code,
        classes: classes,
        time: time,
        room: room,
        vacancy: vacancy,
        swapcourse: swapcourse,
      });
    });
    resolve(datacontain);
  });
}

function login(account, password) {
  let param = {
    username: account,
    password: password,
  };
  return new Promise(function (resolve, reject) {
    store.set("userlogin", param);
    new requestData("login").requestToPy(param).then((res) => {
      resolve(res);
    });
  });
}

// function checkstat() {
//     let n = new Date();
//     if ()
// }
