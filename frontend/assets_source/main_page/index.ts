import './style.css'
import {EchoGrpcApiEchoGrpcPostData} from '../../back_interface_endpoint/types.gen.ts'
import {DefaultService} from '../../back_interface_endpoint/services.gen.ts'
import { setupCounter } from './counter.ts'
const greeting: string = "Hello, World!";
console.log(greeting);

const data: EchoGrpcApiEchoGrpcPostData = {
  requestBody: {
      name: "Alice"
  }
};

DefaultService.echoGrpcApiEchoGrpcPost(data)
  .then(response => {
      console.log(response.message); // Выводим сообщение из ответа
  })
  .catch(error => {
      console.error(error); // Обрабатываем ошибку, если она есть
  });
console.log(data)

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <h1 >Vite + TypeScript</h1>
    <div class="card">
      <button id="counter" type="button"></button>
    </div>
    <p class="read-the-docs">
      Click on the Vite and TypeScript logos to learn more
    </p>
  </div>
`

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
