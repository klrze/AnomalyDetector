package com.anomaly.backend.repository;

import com.anomaly.backend.entity.experiment_log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface experiment_repository extends JpaRepository<experiment_log, Long> {

  List<experiment_log> findByChannel(String channel);

}