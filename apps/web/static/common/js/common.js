    const commonAjaxToJson = async (url, method, params, f = function(){}) => {
        let csrf_token = document.querySelector("meta[name='csrf-token']").getAttribute('content')
		let data = null;
		if("GET" == method.toUpperCase()){
			try {
				const fetchObj = {
					method: "GET",
					headers: {
					    "X-CSRFToken": csrf_token,
						'Content-Type': 'application/json'
					}
    			};
				if (params != null) {
					if( params != {}) {
						url = url +'?'+ new URLSearchParams(params);
					}
				};
				const init = await fetch(url, fetchObj);
				data = await init.json();
			} catch(exc) {
				console.warn(exc);
			}
		}
		else if ("POST" == method.toUpperCase()) {
			if (params == null) {
				params = {};
			}
			const fetchObj = {
				method: "POST",
				headers: {
					"X-CSRFToken": csrf_token,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(params)
			}
			const init = await fetch(url, fetchObj);
			data = await init.json();
		}
		else{
			console.error("GET, POST 형식만 지원합니다.");
		}
		f(data);
	}

	const commonAlert = (text, title, status) => {
        new Notify ({
            status: status,
            title: title,
            text: text,
            effect: 'fade',
            speed: 300,
            customClass: null,
            customIcon: null,
            isIcon: true,
            isCloseButton: true,
            autoclose: false,
            autotimeout: 3000,
            gap: 20,
            distance: 20,
            type: 1,
            position: 'right bottom'
		})
	}