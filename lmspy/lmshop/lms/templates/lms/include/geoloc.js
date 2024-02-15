const glocate = () => {
    const gloc_options = {
        enableHighAccuracy: true,
        timeout: {{param_value_gloc_timeout}},
        maximumAge: 0,
    };
    const gloc_success = pos => {
        let crd = pos.coords;
        __api_call__('{% url "api:set_location" %}', {
            latitude: crd.latitude,
            longitude: crd.longitude,
            accuracy: crd.accuracy
        }, result => {});
    };
    const gloc_error = err => {
        console.warn(`ERROR(${err.code}): ${err.message}`);
        __api_call__('{% url "api:set_location" %}', {
            latitude: {{param_value_default_latitude}},
            longitude: {{param_value_default_longitude}},
            accuracy: 100.0
        }, result => { });
    };
    navigator.geolocation.getCurrentPosition(gloc_success, gloc_error, gloc_options);
};