const b5toastContainerElement = document.getElementById("toast-container");

const b5toast = {
	delayInMilliseconds: 5000,
	htmlToElement: function (html) {
		const template = document.createElement("template");
		html = html.trim();
		template.innerHTML = html;
		return template.content.firstChild;
	},
	show: function (color, title, message, delay) {
		title = title ? title : "";
		if (color == "warning") {
			txt_color = "black";
		}
		else{
			txt_color = "white";
		}
		const html = `
		<div class="toast align-items-center mt-1 text-${txt_color} bg-${color} border-0" role="alert" aria-live="assertive" aria-atomic="true">
			<div class="d-flex">
				<div class="toast-body">
					<b>${title}</b>
					<div><i>${message}</i></div>
				</div>
				<button type="button" class="btn-close btn-close-${txt_color} me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
			</div>
		</div>`;
		const toastElement = b5toast.htmlToElement(html);
		b5toastContainerElement.appendChild(toastElement);
		const toast = new bootstrap.Toast(toastElement, {
			delay: delay?delay:b5toastdelayInMilliseconds,
			animation: true
		});
		toast.show();
		setTimeout(() => toastElement.remove(), delay?delay:b5toastdelayInMilliseconds + 3000); // let a certain margin to allow the "hiding toast animation"
	},
};