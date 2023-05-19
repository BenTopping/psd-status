import { Buffer } from "buffer";

// A function to test the validity of a jwt
export function isValidJwt(jwt) {
  if (!jwt || jwt.split(".").length < 3) {
    return false;
  }
  const data = JSON.parse(Buffer.from(jwt.split(".")[1], "base64").toString());
  const exp = new Date(data.exp * 1000);
  const now = new Date();
  return now < exp;
}
