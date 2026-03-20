const fs = require('fs'), path = require('path'), os = require('os');
const STORE = path.join(os.homedir(), '.lark-mcp-keychain.json');
const load = () => { try { return fs.existsSync(STORE) ? JSON.parse(fs.readFileSync(STORE,'utf8')) : {}; } catch(e){return{};} };
const save = s => fs.writeFileSync(STORE, JSON.stringify(s,null,2), {mode:0o600});
const k = (svc,acc) => `${svc}::${acc}`;
const chk = (v,n) => { if(!v||!v.length) throw new Error(n+' is required.'); };
module.exports = {
  getPassword:(svc,acc)=>{chk(svc,'Service');chk(acc,'Account');return Promise.resolve(load()[k(svc,acc)]||null);},
  setPassword:(svc,acc,pw)=>{chk(svc,'Service');chk(acc,'Account');chk(pw,'Password');const s=load();s[k(svc,acc)]=pw;save(s);return Promise.resolve();},
  deletePassword:(svc,acc)=>{chk(svc,'Service');chk(acc,'Account');const s=load(),existed=k(svc,acc) in s;delete s[k(svc,acc)];if(existed)save(s);return Promise.resolve(existed);},
  findPassword:(svc)=>{chk(svc,'Service');const s=load(),p=`${svc}::`;for(const k of Object.keys(s))if(k.startsWith(p))return Promise.resolve(s[k]);return Promise.resolve(null);},
  findCredentials:(svc)=>{chk(svc,'Service');const s=load(),p=`${svc}::`,r=[];for(const k of Object.keys(s))if(k.startsWith(p))r.push({account:k.slice(p.length),password:s[k]});return Promise.resolve(r);}
};
