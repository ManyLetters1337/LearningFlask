angular.module('constansApiUrls', [])

.constant('CONSTANS_URLS', CONSTANS_URLS());

function CONSTANS_URLS(){
    return {
        users: `http://` + window.location.host + `/api/users/`,
        userById: `http://` + window.location.host + `/api/users/id/`,
        userProjects: `http://` + window.location.host + `/api/users/projects/`,
        userNotes: `http://` + window.location.host + `/api/users/notes/`,
        projects: `http://` + window.location.host + `/api/projects/all_projects`,
        project: `http://` + window.location.host + `/api/projects/`,
        statistic: `http://` + window.location.host + `/api/projects/statistics`,
        notes: `http://` + window.location.host + `/api/notes/all`,
        note: `http://` + window.location.host + `/api/notes/`,
        userNoteStat: `http://` + window.location.host + `/api/users/statistics/`
    };
}

