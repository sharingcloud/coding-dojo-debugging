function check_code (url, entry) {
  const csrftoken = $("input[name=csrfmiddlewaretoken]").val()

  return $.ajax({
    url: url,
    method: 'POST',
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: {
      code: entry,
    }
  });
}
