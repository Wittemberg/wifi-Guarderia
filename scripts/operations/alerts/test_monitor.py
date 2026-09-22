import unittest
from monitor import evaluate
class EvaluationTests(unittest.TestCase):
 def setUp(self):
  self.now=2000000000
  self.h={'backup_active_state':'inactive','backup_service_result':'success','last_attempt_ok':True,'offsite_current':True,'last_verified_remote_at':'2033-05-18T03:33:20+00:00'}
 def test_healthy(self):self.assertEqual(evaluate(self.h,self.now,self.now),[])
 def test_stale_heartbeat_overrides_old_health(self):self.assertEqual(evaluate(self.h,self.now-901,self.now),['heartbeat_ausente_15min'])
 def test_missing_heartbeat(self):self.assertEqual(evaluate({},None,self.now),['heartbeat_ausente_15min'])
 def test_failed_upload(self):
  self.h.update(offsite_current=False,last_attempt_ok=False)
  self.assertIn('falha_backup',evaluate(self.h,self.now,self.now));self.assertIn('copia_s3_atual_nao_verificada',evaluate(self.h,self.now,self.now))
 def test_mid_backup_does_not_report_upload_in_progress(self):
  self.h.update(backup_active_state='activating',offsite_current=False,last_attempt_ok=False)
  self.assertEqual(evaluate(self.h,self.now,self.now),[])
 def test_long_running_backup_does_not_hide_overdue(self):
  self.h.update(backup_active_state='activating',last_verified_remote_at='2020-01-01T00:00:00+00:00')
  self.assertIn('backup_s3_sem_verificacao_26h',evaluate(self.h,self.now,self.now))
 def test_stopped_service_failure_overrides_stale_success_file(self):
  self.h['backup_service_result']='exit-code'
  self.assertIn('falha_backup',evaluate(self.h,self.now,self.now))
 def test_exact_thresholds(self):
  self.assertEqual(evaluate(self.h,self.now-900,self.now),['heartbeat_ausente_15min'])
  self.assertIn('backup_s3_sem_verificacao_26h',evaluate(self.h,self.now+93600,self.now+93600))
if __name__=='__main__':unittest.main()
