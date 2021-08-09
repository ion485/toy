function naverLogin() {
    response_type = 'code'
    client_id = 'HGcrLuWGZEBnn_X1HsZz'
    redirect_uri = 'http://localhost:8000/user/login/social/naver/callback/'
    state = document.querySelector('[name=csrfmiddlewaretoken]').value

    url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=HGcrLuWGZEBnn_X1HsZz&redirect_uri=' + encodeURIComponent(redirect_uri) + '&state=' + encodeURIComponent(state)

    location.replace(url)
}

function kakaoLogin() {
    response_type = 'code'
    client_id = '9a9ab333b1c1d2d29edfe226aaf707c6'
    redirect_uri = 'http://localhost:8000/user/login/social/kakao/callback/'
    state = document.querySelector('[name=csrfmiddlewaretoken]').value

    url = 'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=9a9ab333b1c1d2d29edfe226aaf707c6&redirect_uri=' + encodeURIComponent(redirect_uri) + '&state=' + encodeURIComponent(state)
    //url = 'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=9a9ab333b1c1d2d29edfe226aaf707c&redirect_uri=' + redirect_uri

    location.replace(url)
}
