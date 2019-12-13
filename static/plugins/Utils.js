import {ViewChart} from './Chart.js';

class UtilsClass {
    /*
    Get data from api
    */
  makeRequest(method, url, callback) {
     let xhr = new XMLHttpRequest();

     xhr.open(method, url, false);
     try {
        xhr.send();
        if (xhr.status != 200) {
          alert(`Error ${xhr.status}: ${xhr.statusText}`);
            }
        else {
            callback(JSON.parse(xhr.responseText));
            }
        } catch(err) {
            alert("Request failed");
        }
    }
}

let Utils = new UtilsClass();

export {Utils};
